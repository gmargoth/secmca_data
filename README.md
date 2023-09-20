# secmca_data
Este código descarga el Tipo de Cambio Nominal Mensual (TCN) y el Índice de Precios al Consumidor (IPC) de los países miembros del SECMCA.

Por ejemplo:

```python
serie = "TCN"
start_year, end_year = 1990, 2023
country_list =  ["Costa Rica", "El Salvador","Guatemala","Honduras","Nicaragua","República Dominicana","Panamá"]
df = secmca_download_csv(serie, start_year, end_year, country_list)
# ...
