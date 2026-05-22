# PokéSDK

Lightweight **ETL SDK** for the [PokéAPI](https://pokeapi.co/).

```
Extract → Transform → Load
```

## Install

```bash
pip install pokesdk-0.1.0-py3-none-any.whl
```

## Quick start

```python
import pokesdk

# Full pipeline – returns a DataFrame
df = pokesdk.run(['pikachu', 'charmander', 'bulbasaur'])
print(df.head())

# Save directly to CSV
pokesdk.run(
    ['pikachu', 'charmander'],
    output_format='csv',
    output_path='pokemon.csv',
)

# Use individual ETL layers
raw  = pokesdk.get_pokemon('mewtwo')          # Extract
row  = pokesdk.transform_pokemon(raw)          # Transform (single)
df   = pokesdk.transform_batch([raw])          # Transform (batch)
pokesdk.to_json(df, 'mewtwo.json')             # Load
```

## Available fields

| Field | Description |
|---|---|
| `id` | National Pokédex number |
| `name` | Lowercase name |
| `height_dm` | Height in decimetres |
| `weight_hg` | Weight in hectograms |
| `base_exp` | Base experience yield |
| `types` | List of type names |
| `abilities` | List of abilities (`*` = hidden) |
| `stat_hp` … `stat_speed` | Base stats |
| `sprite_url` | Front default sprite |
| `artwork_url` | Official artwork |

Filter with `fields=[...]`:

```python
df = pokesdk.run(['pikachu'], fields=['id', 'name', 'types', 'stat_hp'])
```

## Error handling

```python
from pokesdk import PokemonNotFoundError

try:
    pokesdk.run(['missingno123'], skip_errors=False)
except PokemonNotFoundError as e:
    print(e)
```
