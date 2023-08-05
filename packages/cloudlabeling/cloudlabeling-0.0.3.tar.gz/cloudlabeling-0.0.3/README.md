# cloudlabeling API
API call for cloudlabeling.org

## How to install (pip)

```bash
conda create -n cloudlabeling python pip
pip install cloudlabeling
```

## How to use (Python)

```python
from cloudlabeling import cloudlabeling

cloud_labeler = cloudlabeling.CloudLabeling()

results = cloud_labeler.infer_remotely(image_path, project_id="MSCOCO")
```
