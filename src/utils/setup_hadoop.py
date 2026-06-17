import os
import urllib.request
import logging
from utils.initialize_logging import initialize_logging

initialize_logging()
logger = logging.getLogger("HadoopSetup")

def ensure_hadoop_setup():
    """
    Garante que o HADOOP_HOME exista e contenha os binários necessários para Windows.
    """
    hadoop_home = r'C:\hadoop'
    hadoop_bin = os.path.join(hadoop_home, 'bin')
    
    base_url = "https://github.com/cdarlint/winutils/raw/master/hadoop-3.3.0/bin/"
    files_to_download = ["winutils.exe", "hadoop.dll"]

    if not os.path.exists(hadoop_bin):
        logger.info(f"Criando diretório Hadoop em: {hadoop_bin}")
        os.makedirs(hadoop_bin, exist_ok=True)

    for file in files_to_download:
        file_path = os.path.join(hadoop_bin, file)
        if not os.path.exists(file_path):
            url = base_url + file
            try:
                logger.info(f"Baixando {file} para {file_path}...")
                urllib.request.urlretrieve(url, file_path)
                logger.info(f"Download de {file} concluído.")
            except Exception as e:
                logger.error(f"Erro ao baixar {file}: {e}")
                raise

    os.environ['HADOOP_HOME'] = hadoop_home
    
    if hadoop_bin not in os.environ['PATH']:
        os.environ['PATH'] = hadoop_bin + os.pathsep + os.environ['PATH']
    
    logger.info("Ambiente Hadoop configurado com sucesso.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    ensure_hadoop_setup()