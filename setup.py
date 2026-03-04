#!/usr/bin/env python
import subprocess

from setuptools import setup, find_packages
from setuptools.command.install import install

__version__ = "2.0.0"

class CustomInstallCommand(install):

    def install_requirements(self):
        #subprocess.check_call(["conda", "install", "-c", "conda-forge", "rdkit", "xgboost", "pandas", "oddt", "-y"])
        #subprocess.check_call(["conda", "install", "-c", "openeye", "openeye-toolkits", "-y"])
        # subprocess.check_call(["pip", "install", "git+https://github.com/BioPandas/biopandas.git"])
        pass
        
    def install_pyrosetta(self):
        #subprocess.check_call(["pip", "install", "pyrosetta-installer"])
        #subprocess.check_call(["python", "-c", "import pyrosetta_installer; pyrosetta_installer.install_pyrosetta()"])
        pass
        
    def install_luna(self):
        subprocess.check_call(["pip", "install", "git+https://github.com/gandrianov/LUNA.git"])

    def install_pocketdruggability(self):
        subprocess.check_call(["pip", "install", "git+https://github.com/gandrianov/PocketDruggability.git"])

    def run(self):
        # Run the standard install process
        install.run(self)
        self.install_requirements()
        self.install_pyrosetta()
        self.install_luna()      
        self.install_pocketdruggability()

setup(
    name="vScreenML",
    version=__version__,
    description="ML classifier for rescoring of virtual screening hits to prune out false positives",
    author="Grigorii Andrianov, Yusuf Adeshina and John Karanicolas",
    author_email="grigorii.andrianov@gmail.com",
    url="https://github.com/gandrianov/vScreenML",
    license="MIT",
    packages=find_packages(),
    package_data={"":["utils/*.txt",
                      "models/*",
                      "data/*",
                      "external/STRAIN/TL_2.1_VERSION_6.xml",
                      "external/generic_potential/*.json",
                      "external/binana/*.md"]},
    include_package_data=True,
    install_requires=open('requirements.txt', 'r').readlines(),
    cmdclass={
        'install': CustomInstallCommand,
    },
    entry_points="""
        [console_scripts]
        vscreenml_calculate_features=vScreenML.main:calculate_features
        vscreenml_minimize_complex=vScreenML.main:minimize_pdb_complex
        vscreenml_mol2params=vScreenML.utils.mol2genparams_utils:run_mol2params
        vscreenml_openeye_assigncharges=vScreenML.utils.openeye_utils:assign_charges
        vscreenml_predict_score=vScreenML.utils.xgboost_utils:predict_vscreenml_score
        vscreenml_train_model=vScreenML.utils.xgboost_utils:train_model
        """,
    keywords=['cheminformatics', 'virtual screening'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
