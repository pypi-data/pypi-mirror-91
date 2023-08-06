## lambdata
An extension for a Pandas Data Frame.

## Motivation
This is a Lambda School project.

## Installation
`pip install lambdata_bcd`

## Tests
`python3 lambdata_tests.py`

## How to use:
```python
import pandas as pd # Pandas is required
from lambdata.helper_df import HelperDataFrame

data = [['tom', 10], ['nick', 15], ['juli', 14]] 
  
# Create the Pandas Data Frame 
df = pd.DataFrame(data, columns = ['Name', 'Age'])

# Create Helper Data Frame
hdf = HelperDataFrame(df)

# Shuffle the rows in a data frame
hdf.randomize()

```

## License
