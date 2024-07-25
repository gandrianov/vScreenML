vScreenML (v2)
==============================

Python-based package of [original implementation](https://github.com/karanicolaslab/vscreenml) of [VScreenML](https://www.pnas.org/content/117/31/18477). 

**Installation**

To install the package and its dependencies, use the following pip command:

```
pip install git+https://github.com/gandrianov/vScreenML.git
```

**Usage**

Before any predictions, we **strongly recommend** to minimize predicted protein-ligand complex in PyRosetta and only then calculate features for classification. This allows to keep information consistent with training set and bypass possible out-of-distribution problems.

**Preparation of predicted model**

- **Ligand parameterization**

At the first step, it needs to generate PDB and param file using alone ligand structure in MOL2 format. Partial charges of ligand atoms should be included into MOL2 file and they can be calculated by [OpenBabel](https://openbabel.org/docs/Command-line_tools/babel.html) or [OpenEye](https://docs.eyesopen.com/toolkits/python/quacpactk/examples_summary_assigncharges.html)

```
vscreenml_mol2params -s <LIGAND>.mol2 \
                     --prefix=<LIGAND> \
                     --comment_bonds=True
```

- **Protein-ligand complex minimization**

This script takes generated on the previous step PDB and params files and uses them for minimization in complex with target protein structure in PDB format. In the end, it generates protein-ligand complex after minimization.

```
vscreenml_minimize_complex -ligand <LIGAND>.pdb \
                           -params <LIGAND>.params \
                           -protein <PROTEIN>.pdb \
                           -output minimized_<COMPLEX>.pdb
```

**Classification of prepared modelc**

- **Features calculation**

We updated [set of features](https://github.com/gandrianov/vScreenML/blob/main/vScreenML/models/DUDE_columns.csv) used for classification by removing non-important for classification and derived from from paid software features. To calculate features, it needs minimized protein-ligand complex, params file of ligand generated previously:

```
vscreenml_calculate_features -pdb-complex minimized_<COMPLEX>.pdb \
                             -ligand-params <LIGAND>.params \
                             -output minimized_<COMPLEX>_features.csv
```

- **VScreenML score prediction**

Before prediction of class, it will be reasonable to check values of `InteractionScore` and `FaAtrInteraction` features. If they are positive or close to zero, then we recommend to remove them from the calculations since model could give incorrect prediction:  

```
vscreenml_predict_score -features minimized_<COMPLEX>_features.csv \
                        -output minimized_<COMPLEX>_predictions.csv
```
