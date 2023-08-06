import os
from pathlib import Path
import numpy as np
import pandas as pd
import dask.bag as db
import dask.dataframe as dd
import h5py
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists
import shutil
import random
from tqdm import tqdm

from ..admin.config import ROOT, MDB, PROJECT_SUBDIRS, MAP_TIMESTAMP
from ..admin.dbio import read_table


################################################################################################################################
## FILES management
################################################################################################################################

################################################################
## list_subdirs
################################################################
def list_subdirs(directory, fullname=False, reverse=False):
    '''
    directory의 1차 하위 디렉토리 목록을 정렬하여 반환
    '''
    
    # for manger module's consistency
    if type(directory) is dict:
        directory = directory['origin']
        
    # do
    if fullname:
        subdirs = sorted(
            [d.path for d in os.scandir(directory) if d.is_dir()],
            reverse = reverse
        )
    else:
        subdirs = sorted(
            [d.name for d in os.scandir(directory) if d.is_dir()],
            reverse = reverse
        )
    
    return subdirs

################################################################
## list_trees
################################################################
def list_trees(directory, exts=None, verbose=False):
    '''
    두 개 이상의 파일(지정된 확장자를 포함한)이 있는 directory의 tree를 반환 - directory structure 파악할 때 사용
    
    params
      directory   탐색할 루트 디렉토리
      ext         탐색할 확장자
      
    return
      <list>      directory structure
    '''

    # for manager module's consistency
    if type(directory) is dict:
        directory = directory['origin']
        
    # set extensions
    if exts is not None:
        # to list if not list
        if type(exts) is not list:
            exts = [exts]
        # strip dot
        exts = [e.strip('.') for e in exts]
    else:
        exts = ['*']
    

    # array of files
    files = np.array(
        list_files(directory, exts)
    )

    # array of levels
    levels = np.array(
        [f.count('/') + 1 for f in files]
    )

    # get directory tree
    trees = dict()
    for level in set(levels):
        files_ = files[levels == level]
        n_ref = len(files_)
        for i in range(1, level-1):
            subdirs = set([f.rsplit('/', i)[0] for f in files_])
            if len(subdirs) != n_ref:
                break
        trees[level] = sorted(subdirs)
    trees = [l for sublist in trees.values() for l in sublist]
    
    # verbose
    if verbose:
        print(f"Meaningful Structure Under {directory}")
        for tree in trees:
            print(f"  - {tree.replace(directory, '.')}")
        
    return trees

################################################################
## make list of files (parallel search using dask)
################################################################
def list_files(directory, exts='*', posix=False):
    '''
    Parallel version (faster) of list files - using Dask
    
    params
      directory   directory to scan
      exts        list of extensions to find
      posix       if true, posix path will be returned
      
    return
      (list of files)   list of posix or string paths
    '''
    # type check
    if type(directory) is dict:
        directory = directory['origin']
    
    # scalar to list
    if type(exts) is not list:
        exts = [exts]
    if type(directory) is not list:
        dirs = [directory]
    
    # revise extensions
    exts = [ext.strip('.') for ext in exts]
    
    # n patternes
    n_exts = len(exts)
    
    # max no. of partitions ~ no. of CPUs x 2
    n_max = os.cpu_count()
    
    # get partitions
    while len(dirs) * n_exts < n_max:
        # scandir
        dirs_ = [d for subdirs in dirs for d in os.scandir(subdirs)]
        n_files = len([f for f in dirs_ if f.is_file()])
        # break if meet files
        if n_files > 0:
            break
        # update dirs
        dirs = dirs_

    # to dask bag
    dirs = db.from_sequence(
        [':'.join([d.path, f'**/*.{ext}']) for ext in exts for d in dirs]
    )
    
    # search
    files = dirs.map(lambda d: [f for f in Path(d.split(':')[0]).glob(d.split(':')[-1])])
    files = files.compute()
    
    # return posix path if posix is True
    if posix:
        files = [f for fs in files for f in fs]
    else:
        files = [str(f) for fs in files for f in fs]
    
    return files

################################################################
## make list of extensions
################################################################
def count_extensions(directory):
    '''
    directory 재귀적 탐색하여 확장자 카운트 반환
    '''
    # init
    
    # for manager module's API consistency
    if type(directory) is dict:
        directory = directory['origin']
        
    # search
    files = list_files(directory, '*', posix=True)
    extensions = pd.Series(
        [str(f).rsplit('.', 1)[-1] for f in files if not f.is_dir()],
        name = 'extensions'
    )
    return extensions.value_counts()

################################################################
## check duplicated date
################################################################
def infer_duplicates(files):
    '''
    filename 확인하여 중복 의심되는 index 반환 (사례: augmentated data가 원본에 섞임)
    
    params
      files    <pd.Series> or <list> list of filenames or filepaths
      
    return
      dataframe with fields;
        - is_dups: orginal or copied (추정)
        - is_original: original file (추정)
        - is_copied: copied file (추정)
    '''
    # init
    files = pd.Series(
        [f.rsplit('/', 1)[-1] for f in files],
        name='filename'
    )
    
    # get lengths
    lengths = np.array(
        [len(f.rsplit('.', 1)[0]) for f in files]
    )
    
    # when length is not fixed, duplicates may exist
    if len(set(lengths)) > 1:
        # original files ~ files w/ shortest filename
        min_length = lengths.min()
        shorten = pd.Series(
            [f[:min_length] for f in files], 
            name='shorten'
        )
    
        # update flag
        duplicates = shorten.duplicated(keep=False).to_numpy()
        
        df_flag = pd.DataFrame({
            'filename': files,
            'origin': shorten,
            'is_dups': duplicates,
            'is_original': lengths == min_length,
            'is_copied': (lengths != min_length) & duplicates
        })
        
        return df_flag
        
    else:
        return None

    
################################################################################################################################
## GET PROJECT's SOMETHING
################################################################################################################################

################################################################
## gen_db_dirs
################################################################
def gen_project_db_dirs(project):
    '''
    project의 DB, DIRS를 생성하여 반환
    
    params
      project   project code (예: airpurifier, dishwasher)
      
    return
      DB, DIRS
    '''
    
    #### FIXED VARIABLES ####   
    # project's directories
    project_dir = os.path.join(ROOT, project)
    DIRS = {
        d: os.path.join(project_dir, d) for d in PROJECT_SUBDIRS
    }
    DIRS['root'] = project_dir
    
    # project's database
    db_url = f"sqlite:///{project_dir}/project.db"
    DB = create_engine(db_url)
    
    return DB, DIRS


################################################################
## get_project
################################################################
def get_project(project):
    '''
    준비되어 있는 project의 DB, DIRS를 load
    
    params
      project   project code (예: airpurifier, dishwasher)
      
    return
      DB, DIRS
    '''
    
    DB, DIRS = gen_project_db_dirs(project)
    
    # validation - DIRS
    if not os.path.exists(DIRS['root']):
        print(f"[ERROR] No project '{project}' found. Exit!")
        return
    
    # validation - DB
    if not database_exists(DB.url):
        print(f"[ERROR] No project '{project}' found. Exit!")
        return
    
    return DB, DIRS


################################################################
## project_parser
################################################################
def project_parser(project):
    '''
    사용자 편의용 - project, DB, DIRS 중 하나를 입력하면 tuple(project, DB, DIRS)를 반환
    '''
    # parse
    if type(project) is sqlalchemy.engine.base.Engine:
        project = Path(str(project.url).replace('sqlite:///', '')).parent.name
    elif type(project) is dict:
        project = Path(project['root']).name
    elif type(project) is not str:
        print("ERROR!")
        return

    # get info
    DB, DIRS = get_project(project)
    
    return project, DB, DIRS


################################################################
## list_projects
################################################################
def list_projects(full=False, return_=False):
    '''
    등록되어 있는 프로젝트 목록 반환
    '''
    
    # read table 'project' from mother database
    tbl = read_table(MDB, 'projects')
    
    # shorten
    if not full:
        tbl = tbl[['code', 'name', 'category', 'client', 'contact', 'opened', 'note']]
        
    display(tbl)
    
    # return table if return_
    if return_:
        return tbl


################################################################
## list_lots
################################################################
def list_lots(project, process=None, status=None, verbose=False):
    '''
    지정된 process가 완료된 lot들의 list 반환
    
    params
      DB
      process   ['inventory', 'dataset', 'extract', 'post', 'report']
      forced
      
    return
      (lots_to_update)
    '''
    
    # init
    project, DB, DIRS = project_parser(project)
    
    # read tables from project database
    try:
        history = read_table(DB, 'history')
    except Exception as ex:
        print(f"[ERROR] Cannot load table history - {ex}")
        return
    
    # 아무것도 지정 안하면 df 출력
    SELECT = ['lot', 'extensions', 'n_origin', 'n_valid', 'n_revised', 'added', 'copied', 'extracted', 'posted', 'reported', 'modified']
    if process is None and status is None:
        display(history[SELECT])
        return
    
    # verbose
    if verbose:
        display(history[SELECT])
    
    # all lots
    history = history.set_index('lot')
    lots = sorted(history.index)
    
    # return list of all lots if status is None
    if status is None:
        return lots
    
    # default process is 'extract'
    if process is None:
        process = 'extract'
    
    # map process to timestamp
    try:
        field_stamp = MAP_TIMESTAMP[process]
    except Exception as ex:
        print(f"[ERROR] Process '{process}' is not in {[p for p in MAP_TIMESTAMP.keys()]} - {ex}")
        return
    
    # list complete lots
    lots_complete = []
    for lot in history.index:
        if history.at[lot, field_stamp] is not None:
            if history.at[lot, field_stamp] > history.at[lot, 'modified']:
                lots_complete.append(lot)
    
    # list uncomplete lots
    lots_uncomplete = sorted(set(lots) - set(lots_complete))
    
    # returns
    if status.lower() in ['complete', 'up-to-date']:
        return lots_complete
    elif status.lower() in ['uncomplete', 'modified', 'changed']:
        return lots_uncomplete
    else:
        print("Please Select Status: [None, 'complete', 'modified']")
        return

    
################################################################
## load_dataset
################################################################
def load_rawdata(project, columns=None, compute=True):
    '''
    load extracted raw data of project as pd.DataFrame
    
    params
      project   project_code (e.g. airpurifier, dishwasher)
      compute   if False, it returns dask dataframe
    
    return
      extracted raw data <pd.DataFrame>
    '''
    
    # for manager's consistency
    try:
        project, DB, DIRS = project_parser(project)
    except Exception as ex:
        print(ex)
        return

    # read dataset
    history = read_table(DB, 'history')
    inventory = read_table(DB, 'inventory')

    # list of prepared lots
    lots = list_lots(project, process='extract', status='complete')
    
    # read dataset (parquet) and compute
    files = [os.path.join(DIRS['extract'], f"extracted_{lot}*.parquet") for lot in lots]
    
    # read parquet
    extracted = dd.read_parquet(files, columns=columns)

    # compute if compute
    if compute:
        extracted = extracted.compute().reset_index(drop=True)
    
    return extracted


################################################################
## load_features
################################################################
def load_features(project=None, srcpath=None, custom=None, downloadpath=None, verbose=True):
    '''
    load prepared features.
    
    (NOTE)
    이미 처리된 feature들의 저장소로 HDF5 형식 파일을 사용하고 있습니다.
    HDF5 형식은 데이터를 RAM에 load하지 않고 disk에서 바로 access합니다. 
    RAM 크기에 제한 받지 않고 큰 데이터를 저장할 수 있고, 최초 load가 발생하지 않는 장점이 있습니다.
    다만 disk에 빈번히 access하는 만큼 disk 속도에 큰 영향을 받습니다. NFS(NAS)를 사용하면 더욱 늦어집니다.
    분석 속도를 높이려면 download_path를 지정하여 HDF5를 local에 다운로드 후 load하시면 됩니다.
    만약 SSD가 있다면 download_path로 SSD를 지정하시는 것을 권장합니다.
    
    params
      project        project_code (e.g. airpurifier, dishwasher)
      srcname        srcpath - 사용자 로컬에 저장한 HDF5를 load할 때 사용
      custom         default name (features.hdf5)가 아닌 features를 load할 때 사용
      downloadpath   download path. When it is not None, features will be load after download
    
    return
      extracted raw data <pd.DataFrame>
    '''
    
    if srcpath is None:
        if project is None:
            print('[EXIT] Please set project or srcpath!')
        else:
            # for manager's consistency
            project, DB, DIRS = project_parser(project)    
            # set srcpath
            if custom is None:
                srcpath = os.path.join(DIRS['extract'], 'features.hdf5')
            else:
                srcpath = os.path.join(DIRS['extract'], custom)
    else:
        if project is not None:
            print('[WARNING] If both project and srcpath are given, srcpath will be used.')
    
    # download if download path is not None
    if downloadpath is not None:
        # get size
        size_gb = os.path.getsize(srcpath)/1024/1024/1024
        
        # check before download
        download = True
        maxloop = 3
        
        # is too large?
        if download:
            n=0; chk = 'init'
            if size_gb > 0:
                while (chk not in ['yes', 'no']) and n < maxloop:
                    n += 1
                    chk = input(f"HDF5 file is very large ({size_gb:.1f} GB), download anyway? (yes or no):").lower()
                if chk == 'no':
                    download = False
                
        # already exists?
        if download:
            n=0; chk2 = 'init'
            if os.path.exists(downloadpath):
                while (chk2 not in ['yes', 'no']) and (n < maxloop):
                    n += 1
                    chk2 = input(f"File {downloadpath} exists, overwrite? (yes or no):").lower()
                if chk2 == 'yes':
                    os.remove(downloadpath)
                else:
                    download = False
                
        # download
        if download:
            print(f"Start Download {size_gb:.1f} GB files...", end=" ")
            shutil.copy(srcpath, downloadpath)
            print("DONE!")
            srcpath = downloadpath
                    
    # load
    features = h5py.File(srcpath)
    
    if verbose:
        print(f"Try below commands")
        print(f"  - Y = features['Y'][:]")
        print(f"  - Xmel = features['mel'][:]")
        print(f"  - Xobps = features['obps'][:]")
        print(f"  - F = np.array([x.decode('utf-8') for x in features['filename'][:]])")
        print("")
        print(f"If you need more information, execute 'icu.info_hdf5(features)'.")
        print("")
    
    return features


################################################################
## load_features
################################################################
def info_hdf5(features, feature=None):
    '''
    HDF5의 정보를 쉽게 확인
    '''
    # prep description if exists
    get_desc = lambda feature: features[feature].attrs['desc'] if 'desc' in features[feature].attrs.keys() else 'no description.'
    
    # feature를 지정하지 않으면 전체 dataset의 이름을 출력
    if feature is None:
        rj = max([len(feature) for feature in features.keys()])
        print(f"You have {len(features.keys())} dataset in features.hdf5;")
        for feature in features.keys():
            dataset_name = f"'{feature}'".ljust(rj+2)
            print(f"  - {dataset_name}: {get_desc(feature)}")
        print("")
        print(f"If you need more information, execute 'icu.info_hdf5(features, dataset_name)'.")
    
    # feature를 지정하면 해당 dataset의 정보를 출력
    else:
        print(f"'{feature}': {get_desc(feature)}")
        print(f"  - shape {features[feature].shape}")
        print(f"  - properties")
        for prop in features[feature].attrs.keys():
            value = features[feature].attrs[prop]
            if type(value) is np.ndarray:
                if value.ndim > 1 or value.shape[0] > 3:
                    s = f"{type(value)} w/ shape {value.shape}"
            elif type(value) is list:
                if len(value) > 3:
                    s = f"{type(value)} w/ {len(value)} elements; {', '.join([e for e in value[:3]])}, ..."
            else:
                s = value
            print(f"    . {prop}: {s}")


################################################################
## load_project
################################################################
def load_project(project):
    '''
    project의 모든 정보, 데이터를 로드 - 리포트 init 용
    
    return
      project, DB, DIRS, history, inventory, revisions, rawdata, features, Y, L
    
    return info.
      Y   encoded label ~ 0, 1, ...
      L   string label ~ OK, NG, ...
      F   filenames
    '''
    # mother database
    info = (
        pd.read_sql_table('projects', MDB)
        .set_index('code')
        .loc[project, :]
        .to_dict()
    )

    # project urls
    project, DB, DIRS = project_parser(project)

    # get project tables
    history = read_table(DB, 'history')
    inventory = read_table(DB, 'inventory')
    revisions = read_table(DB, 'inventory')

    # data
    rawdata = load_rawdata(project)
    features = load_features(project, verbose=False)

    # parse features
    Y = features['Y'][:]
    decoder = eval(features['Y'].attrs['decoder']) if 'decoder' in features['Y'].attrs.keys() else None
    if decoder is not None:
        if 'ok' not in decoder[0].lower():
            print("[WARNING] Coded class 0 is not OK class! Please check!")
        L = np.array([decoder[y] for y in features['Y'][:]])
    else:
        L = Y
    F = np.array([f.decode('utf-8') for f in features['filename'][:]])
        
    # prep assets
    assets = pd.read_csv(os.path.join(DIRS['assets'], 'assets.csv'))
    
    return project, DB, DIRS, info, history, inventory, revisions, rawdata, features, Y, L, F, assets


################################################################################################################################
## 
################################################################################################################################

################################################################
## sort_labels
################################################################
def sort_labels(labels):
    '''
    클래스 순서를 정렬
    sort_labels([NG_1, OK, NG_2, OK, NG_1, ...]) -> ['OK', 'NG_1', 'NG_2', 'NG_3']
    '''
    FIRSTCLASS = 'ok'
    INCLASS_REVERSE = False
    
    classes = set(labels)
    head = sorted({l for l in labels if FIRSTCLASS in l.lower()}, reverse=INCLASS_REVERSE)
    tail = sorted({l for l in labels if l not in head}, reverse=INCLASS_REVERSE)
        
    return head+tail

################################################################
## sampling
################################################################
def eda_sampling(tbl, by, n=None, nested=False, sort=True, verbose=True):
    '''
    (예) eda_sampling(df, 'label_origin', n=100, )
    
    by에 지정된 columns로 groupby한 뒤 각 group에서 동일 개수의 sample을 추출.
    EDA 시 OK 개수가 상대적으로 많아 NG의 분포가 가려지는 것을 완화하기 위해 사용.
    
    params
      tbl      <pd.DataFrame>
      by       <str> or <list> groupby할 columns ~ 예: label_origin
      n        n을 지정, n보다 부족한 sample은 최대한의 sample 출력
      nested   True이면 샘플링 결과를 dictionary로 반환. 예, outputs['NG'], outputs['OK'], ...
      sort     True이면 샘플링 결과를 입력 dataframe의 index 순서로 재정렬, default True
    
    return
      <pd.DataFrame>   sampled dataframe (nested=True이면 dictionary of dataframes)
    
    '''
    # multi index available
    if type(by) is not list:
        by = [by]
    
    # dummy index to get series count
    df = tbl.copy(deep=False)
    
    # idxs is sets of multi indices
    summary = df.groupby(by)['filename'].count()
    groups = summary.index
    
    # 가장 적은 sample을 가진 group의 sample 수
    n_min = summary.min()
    
    # message용 rjust 간격
    rj_total = len(str(summary.max()))
    rj_sample = len(str(n))
    
    # sampling n rows for each 'by'
    outputs = dict()
    message = "Sampling Results:"
    for group in groups:
        # if group is multi-index
        if type(group) is tuple: 
            group = list(group)
        # if group is single index
        if type(group) is not list: 
            group = [group]
        
        # sampling from each groups
        df_group = df
        for field, ref in zip(by, group):
            df_group = df_group.loc[df_group[field]==ref, :]
        
        # n이 지정되지 않으면 sample 가장 적은 group의 sample 수를 기준으로
        n_group = len(df_group)
        n_samples = n_min if n is None else min(n_group, n)
        
        # sampling
        df_group = df_group.sample(n=n_samples)
        
        # append message
        message += f"\n  - Group {'/'.join(group)}: {str(n_samples).rjust(rj_sample)} samples / {str(n_group).rjust(rj_total)} total"
        
        # sort if sort
        if sort:
            df_group = df_group.sort_index()
        
        # nested outputs' keys are [level1, level2]
        outputs['/'.join(group)] = df_group
    
    if verbose:
        print(message)
        
    if not nested:
        outputs = pd.concat([v for k, v in outputs.items()])
        if sort:
            outputs = outputs.sort_index()
        
    return outputs


################################################################
# make labels inferred from subdirs
################################################################
def make_labels(data_dir, subdir_structure='label'):
    '''
    subdir_structure: 하위 디렉토리 구조, 예: data_dir이 /dataset일 때
      (예) data_dir='/dataset'인 아래 구조의 subdir_structure는 'channel/label'
      /dataset
          ├ CH1
          │   ├ NG
          │   └ OK
          └ CH2
              ├ NG
              └ OK
      
      /dataset/channel/NG, /dataset/channel/OK로 나뉜 dataset의 subdir_structure='channel/NG'
    '''
    
    exts=["wav", "tdms"]
    
    subdirs = [Path(d) for d in os.scandir(filepath) if os.path.isdir(d)]
    
    files = []
    for subdir in subdirs:
        for ext in exts:
            if fast:
                files.extend(subdir.glob(f"*.{ext.lstrip('.')}"))
            else:
                files.extend(subdir.glob(f"**/*.{ext.lstrip('.')}"))
        
    labels = pd.DataFrame({
        'filename': [f.name for f in files],
        'filepath': [str(f) for f in files],
        'label': [f.parent.name for f in files]
    })
    
    return labels


################################################################
# slice dataframe 
################################################################
def estimate_parquet_size(func, input_, n_samples=100, **kwargs):
    
    TEMP_FILENAME = 'parquet_size_check.parquet'
    
    if type(input_) is not list:
        input_ = list(input_)
    n_total = len(input_)
    samples = random.sample(input_, n_samples)
    
    output = func(samples, **kwargs)
    if type(output) is not pd.DataFrame:
        output = pd.DataFrame(output)
    output.to_parquet(TEMP_FILENAME)
    
    sample_size_mb = os.path.getsize(TEMP_FILENAME)/1024/1024
    required_memory_gb = output.memory_usage(index=True, deep=True).sum()/n_samples*n_total/1024/1024
    n_rows_per_parquet = int(1024 / sample_size_mb * n_samples)
    
    os.remove(TEMP_FILENAME)
    
    print(f"#### Parquet Size Estimation ####")
    print(f" - write 1 parquet per {n_rows_per_parquet} rows (for 1 GB/parquet)")
    print(f" - if you load all {n_total} rows at once, {required_memory_gb:.0f} GB will be required")
    
    return n_rows_per_parquet, required_memory_gb


################################################################
# slice dataframe 
################################################################
def slice_df(df, chunk_size=None, n_chunks=None):
    '''
    input
    :df: dataframe
    :chunk_size: 
    :n_chunks:
    
    return
    dict(i:padded_string, chunk:dataframe)
    '''
    
    len_df = len(df)
    
    if n_chunks and not chunk_size:
        chunk_size = np.ceil(len_df / n_chunks).astype(int)
    if chunk_size and not n_chunks:
        n_chunks = np.ceil(len_df / chunk_size).astype(int)
    else:
        print("set a parameter between chunk_size and n_chunks")
        return None
    
    n_zfill = np.trunc(np.log10(n_chunks)).astype(int) + 1
    
    return {f"{str(i+1).zfill(n_zfill)}": df[i*chunk_size:(i+1)*chunk_size].reset_index(drop=True) for i in np.arange(0, n_chunks)}


################################################################
# encode labels
################################################################
def encode_labels(labels, reverse=True, verbose=True):
    '''
    (NG, OK) become (1, 0) if reverse else (0, 1)
    (NG1, NG2, NG3, OK) becomes (3, 2, 1, 0) if reverse else (0, 1, 2, 3)
    
    params
      labels   list of labels in string
      reverse
      verbose
      
    return
      <list>, <dict>, <dict>   encoded labels, encoder, decoder
    '''
    names = sort_labels(labels)
    encoder = {name: code for code, name in enumerate(names)}
    decoder = {code: name for code, name in enumerate(names)}
    
    labels_encoded = [encoder[x] for x in labels]
    
    if verbose:
        print(f'<LABELS> {len(names)} classes')
        print(f'encoder = {encoder}')
        print(f'decoder = {decoder}')
        print('')
        
    return labels_encoded, encoder, decoder


################################################################
# encode labels
################################################################

# (수정!) df copy해서 쓸 것
def one_hot_encode_labels(labels, class_nothing='nothing', reverse=True, verbose=True):
    '''
    binary cross entropy 사용을 위한 one_hot_encoding
    class_nothing class 지정하면 해당 class는 (0, 0, ..., 0) 값을 가짐 (예를 들어 OK를 OK으로 분류하는 것이 아니라 아무것도 아님으로 분류)
    '''
    names = sorted(set('|'.join(labels['label'].tolist()).split('|')), reverse=reverse)
    if class_nothing in names:
        names.remove(class_nothing)
    n_classes = len(names)
    encoder = {name: code for code, name in enumerate(names)}
    decoder = {code: name for code, name in enumerate(names)}
    
    #### one hot encoding
    labels_encoded = labels.copy()
    for i in labels_encoded.index:
        label_vector = n_classes * [0]
        classes = labels_encoded.at[i, 'label'].split('|')
        if class_nothing in classes:
            classes.remove(class_nothing)
        for c in classes:
            label_vector[encoder[c]] = 1
        labels_encoded.at[i, 'label'] = '|'.join([str(e) for e in label_vector])
    
    if verbose:
        print(f'<LABELS> {n_classes} classes')
        print(f'encoder = {encoder}')
        print(f'decoder = {decoder}')
        print('')
        
    return labels_encoded, encoder, decoder
      
        
################################################################
# make_confusion_matrix
################################################################
def make_confusion_matrix(truth, predict):
    cm = pd.crosstab(truth, predict)
    for l in cm.index:
        if l not in cm.columns:
            cm[l] = 0
    return cm[cm.index]
