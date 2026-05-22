import pokesdk

# Gen 1 completa → DataFrame
df = pokesdk.run_generation(1)

# Gen 1 con campos específicos → CSV
pokesdk.run_generation(
    generation=1,
    fields=['id', 'name', 'types', 'weight_hg', 'stat_hp', 'stat_speed'],
    output_format='csv',
    output_path='pokemon.csv'
)

# También puedes solo obtener los nombres
nombres = pokesdk.get_generation_names(1)