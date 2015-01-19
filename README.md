# Streak CRM API in Python 3
## streak-crm-python

Realizes API described here https://www.streak.com/api

Usage:

```python
# initiate Connector
streak = StreakConnector(YOUR_API_KEY)

# call methods

pipelines_list = streak.pipeline_get_all()
# <Pipeline: 'New clients'>, <Pipeline: 'Calls'>

pipelne_key = pipelines_list[0].pipelineKey
new_box = streak.box_create(pipeline_key, {'name': 'my new box'}
box_list = streak.box_get_all_in_pipeline(pipeline_key)
# <Box: my new box>

```
