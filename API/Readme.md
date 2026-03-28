# API Usuarios

Esta API permite realizar operaciones CRUD sobre los usuarios de la aplicación.

## Base URL


http://localhost:3000/api/usuarios


---

## Leer usuarios

- **Método:** `GET`
- **URL:** `/`
- **Descripción:** Obtiene la lista de todos los usuarios.
- **Ejemplo de solicitud:**

```bash
GET http://localhost:3000/api/usuarios
Respuesta esperada (JSON):
[
  {
    "nombre": "Juan Pérez",
    "email": "juanp@gmail.com",
    "edad": 25,
    "rol": "cliente"
  },
  {
    "nombre": "María López",
    "email": "marial@gmail.com",
    "edad": 30,
    "rol": "cliente"
  }
]
Crear usuarios
Método: POST
URL: /multiple
Descripción: Permite crear varios usuarios a la vez enviando un arreglo de objetos JSON.
Ejemplo de solicitud:
[
  {"nombre": "Juan Pérez", "email": "juanp@gmail.com", "edad": 25, "rol": "cliente"},
  {"nombre": "María López", "email": "marial@gmail.com", "edad": 30, "rol": "cliente"},
  {"nombre": "Carlos Gómez", "email": "carlosg@gmail.com", "edad": 28, "rol": "administrador"}
]
Respuesta esperada (JSON):
{
  "message": "Usuarios creados correctamente",
  "usuarios": [
    {"nombre": "Juan Pérez", "email": "juanp@gmail.com", "edad": 25, "rol": "cliente"},
    {"nombre": "María López", "email": "marial@gmail.com", "edad": 30, "rol": "cliente"}
  ]
}
Modificar usuario
Método: PUT
URL: /:id
Descripción: Actualiza los datos de un usuario específico usando su id.
Parámetros de ruta:
id → ID del usuario a actualizar.
Ejemplo de solicitud:
{
  "nombre": "Juan Pérez",
  "email": "juanp@gmail.com",
  "edad": 26,
  "rol": "cliente"
}
PUT http://localhost:3000/api/usuarios/69c6e6b22bd7fb5b68f50c4c
Respuesta esperada (JSON):
{
  "message": "Usuario actualizado correctamente",
  "usuario": {
    "nombre": "Juan Pérez",
    "email": "juanp@gmail.com",
    "edad": 26,
    "rol": "cliente"
  }
}
Eliminar usuario
Método: DELETE
URL: /:id
Descripción: Elimina un usuario específico usando su id.
Parámetros de ruta:
id → ID del usuario a eliminar.
Ejemplo de solicitud:
DELETE http://localhost:3000/api/usuarios/69c6e6b22bd7fb5b68f50c55
Respuesta esperada (JSON):
{
  "message": "Usuario eliminado correctamente"
}
Notas
Todos los endpoints devuelven respuestas en formato JSON.
Para crear o actualizar usuarios, asegúrate de enviar todos los campos requeridos (nombre, email, edad, rol).
Recursos adicionales
Colección Postman