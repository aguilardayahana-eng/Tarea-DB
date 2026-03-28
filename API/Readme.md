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
```
## Crear usuarios
**Método:** POST
**URL:** /multiple
**Descripción:** Permite crear varios usuarios a la vez enviando un arreglo de objetos JSON.
**Ejemplo de solicitud:**
```bash
[
  {"nombre": "Juan Pérez", "email": "juanp@gmail.com", "edad": 25, "rol": "cliente"},
  {"nombre": "María López", "email": "marial@gmail.com", "edad": 30, "rol": "cliente"},
  {"nombre": "Carlos Gómez", "email": "carlosg@gmail.com", "edad": 28, "rol": "administrador"}
]
```

## Respuesta esperada (JSON):
```bash
{
  "message": "Usuarios creados correctamente",
  "usuarios": [
    {"nombre": "Juan Pérez", "email": "juanp@gmail.com", "edad": 25, "rol": "cliente"},
    {"nombre": "María López", "email": "marial@gmail.com", "edad": 30, "rol": "cliente"}
  ]
}
```
## Modificar usuario
**Método:** PUT
**URL:** /:id
**Descripción:** Actualiza los datos de un usuario específico usando su id.
**Parámetros de ruta:**
***id → ID del usuario a actualizar.***
**Ejemplo de solicitud:**
```bash
{
  "nombre": "Juan Pérez",
  "email": "juanp@gmail.com",
  "edad": 26,
  "rol": "cliente"
}
```

```bash

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
```
## Eliminar usuario
**Método:** DELETE
**URL:** /:id
**Descripción:** Elimina un usuario específico usando su id.
**Parámetros de ruta:**
***id → ID del usuario a eliminar.***
**Ejemplo de solicitud:**
DELETE http://localhost:3000/api/usuarios/69c6e6b22bd7fb5b68f50c55
Respuesta esperada (JSON):
```bash
{
  "message": "Usuario eliminado correctamente"
}
```
___________________________________________________________________________________

# 📄 API de Ventas

## 📌 Descripción
Esta API permite la gestión de ventas de prendas, proporcionando operaciones básicas de tipo CRUD (Crear, Leer, Actualizar y Eliminar).

---

## 🔗 URL Base
http://localhost:3000/api/ventas


---

## 📚 Endpoints

### ➕ Crear una venta

- **Método:** `POST`
- **Endpoint:** `/api/ventas`

#### 📥 Cuerpo de la solicitud
```json
{
  "prenda": "Camiseta",
  "marca": "Nike",
  "cantidad": 2,
  "precio": 15000,
  "fecha": "2026-03-23"
}
📤 Respuesta esperada
{
  "mensaje": "Venta creada correctamente"
}
```
## 📖 Obtener todas las ventas
- **Método:** GET
- **Endpoint:** /api/ventas
```json
📤 Respuesta esperada

[
  {
    "_id": "ID",
    "prenda": "Camiseta",
    "marca": "Nike",
    "cantidad": 2,
    "precio": 15000,
    "fecha": "2026-03-23"
  }
]
```
## ✏️ Actualizar una venta
- **Método:** PUT
- **Endpoint:** /api/ventas/{id}
```json
📥 Cuerpo de la solicitud

{
  "producto": "Camisa",
  "precio": 30,
  "cantidad": 3
}
```
📌 Ejemplo de URL
http://localhost:3000/api/ventas/69c1f731352d6c012f3ae123
```json
📤 Respuesta esperada

{
  "mensaje": "Venta actualizada correctamente"
}
```
## ❌ Eliminar una venta
- **Método:** DELETE
- **Endpoint:** /api/ventas/{id}

## 📌 Ejemplo de URL
http://localhost:3000/api/ventas/69c1f731352d6c012f3ae123
```json
📤 Respuesta esperada
{
  "mensaje": "Venta eliminada correctamente"
}
```
## ⚙️ Consideraciones
El servidor debe estar ejecutándose en el puerto 3000.
Los identificadores (_id) son generados por la base de datos (MongoDB).
Se recomienda utilizar herramientas como Postman para probar los endpoints.
## ➕ Crear múltiples marcas

**Método:** `POST`  
**Endpoint:** `/api/marcas/multiple`

**Descripción:** Permite registrar varias marcas en una sola solicitud.

### 📥 Cuerpo de la solicitud
```json
[
  { "nombre": "Nike", "pais": "USA" },
  { "nombre": "Adidas", "pais": "Alemania" },
  { "nombre": "Puma", "pais": "Alemania" },
  { "nombre": "Reebok", "pais": "USA" },
  { "nombre": "Under Armour", "pais": "USA" },
  { "nombre": "New Balance", "pais": "USA" },
  { "nombre": "Vans", "pais": "USA" },
  { "nombre": "Converse", "pais": "USA" },
  { "nombre": "Fila", "pais": "Italia" },
  { "nombre": "Levi's", "pais": "USA" }
]
📤 Respuesta esperada
{
  "message": "Marcas creadas correctamente"
}
📖 Obtener marcas

Método: GET
Endpoint: /api/marcas

📤 Respuesta esperada
[
  {
    "_id": "ID",
    "nombre": "Nike",
    "pais": "USA"
  }
]
✏️ Actualizar marca

Método: PUT
Endpoint: /api/marcas/{id}

📥 Cuerpo de la solicitud
{
  "nombre": "NIKE",
  "pais": "Estados Unidos"
}
📌 Ejemplo de URL

http://localhost:3000/api/marcas/69c6e71e2bd7fb5b68f50c56

📤 Respuesta esperada
{
  "message": "Marca actualizada correctamente"
}
❌ Eliminar marca

Método: DELETE
Endpoint: /api/marcas/{id}

📌 Ejemplo de URL

http://localhost:3000/api/marcas/69c6e71e2bd7fb5b68f50c56

📤 Respuesta esperada
{
  "message": "Marca eliminada correctamente"
}