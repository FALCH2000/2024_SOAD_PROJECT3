tema reserva
suscripciones:
- crear-reserva: filtro attributes.type ="crear-reserva"
- crear-reserva-resultado: filtro attributes.type ="crear-reserva-resultado"

- editar-reserva: filtro attributes.type = "editar-reserva"
- editar-reserva-resultado: filtro attributes.type = "editar-reserva-resultado"

- eliminar-reserva: filtro attributes.type = "eliminar-reserva"
- eliminar-reserva-resultado: filtro attributes.type = "eliminar-reserva-resultado"

// debe funcionar para una en especifico o para varias o devuelve solo las futuras o devuelve solo las reserrvas del pasado
- obtener-reserva:filtro attributes.type = "obtener-reserva"
- obtener-reserva-resultado: filtro attributes.type = "obtener-reserva-resultado"

- obtener-calendario-disponibilidad:filtro attributes.type = "obtener-calendario"
- obtener-calendario-disponibilidad-resultado: filtro attributes.type = "obtener-calendario-resultado"

tema recomendacion
suscripciones:
- obtener-menu: filtro attributes.type = "obtener-menu"
- obtener-menu-resultado: filtro attributes.type = "obtener-menu-resultado"
// debe funcionar con 1 o 2 comidas
- obtener-recomendacion: filtro attributes.type = "obtener-recomendacion"
- obtener-recomendacion-resultado: filtro attributes.type = "obtener-recomendacion-resultado"

tema usuario
- crear-usuario: filtro attributes.type = "crear-usuario"
- crear-usuario-resultado: filtro attributes.type = "crear-usuario-resultado"

- login: filtro attributes.type = "login"
- login-resultado: filtro attributes.type = "login-resultado"

- restablecer-password: filtro attributes.type = "restablecer-password"
- restablecer-password-resultado: filtro attributes.type = "restablecer-password-resultado"


tema admin
- ampliar-disponibilidad-reservas: filtro attributes.type = "ampliar-disponibilidad-reservas"
- ampliar-disponibilidad-reservas-resultado: filtro attributes.type = "ampliar-disponibilidad-reservas-resultado"

gcloud functions deploy obtener-menu --runtime python312 --trigger-topic recomendacion --entry-point obtener_menu --project groovy-rope-416616

487a20c86795045e732cac2bce791ffa7a4a3d5447ef202bc20fc13b477a9c27
