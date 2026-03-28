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
## ___________________________________________________________________________________

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
] ```
```json
📤 Respuesta esperada
{
  "message": "Marcas creadas correctamente"
}
```

## 📖 Obtener marcas

-**Método:** GET
- **Endpoint:** /api/marcas
```json
📤 Respuesta esperada
[
  {
    "_id": "ID",
    "nombre": "Nike",
    "pais": "USA"
  }
]
```
## ✏️ Actualizar marca

-**Método:** PUT
-**Endpoint:** /api/marcas/{id}
```json
📥 Cuerpo de la solicitud
{
  "nombre": "NIKE",
  "pais": "Estados Unidos"
}
```
## 📌 Ejemplo de URL

** http://localhost:3000/api/marcas/69c6e71e2bd7fb5b68f50c56 **
```json

📤 Respuesta esperada
{
  "message": "Marca actualizada correctamente"
}
```

## ❌ Eliminar marca

**Método:** DELETE
**Endpoint:** /api/marcas/{id}

## 📌 Ejemplo de URL

**http://localhost:3000/api/marcas/69c6e71e2bd7fb5b68f50c56**
```json
📤 Respuesta esperada
{
  "message": "Marca eliminada correctamente"
}
```

## 🔗 URL Base
http://localhost:3000/api/prendas

---

## 📖 Obtener prendas

**Método:** `GET`  
**Endpoint:** `/api/prendas`

### 📤 Respuesta esperada
```json
[
  {
    "_id": "ID",
    "nombre": "Camiseta Deportiva",
    "talla": "M",
    "precio": 20,
    "marca": "Nike"
  }
]
```
## ➕ Crear múltiples prendas

**Método:** POST
**Endpoint:** /api/prendas/multiple

Descripción: Permite registrar varias prendas en una sola solicitud.
```json
📥 Cuerpo de la solicitud
[
  { "nombre": "Camiseta Deportiva", "talla": "M", "precio": 20, "marca": "Nike" },
  { "nombre": "Pantalón Jogger", "talla": "L", "precio": 35, "marca": "Adidas" },
  { "nombre": "Sudadera con Capucha", "talla": "XL", "precio": 50, "marca": "Puma" },
  { "nombre": "Chaqueta Impermeable", "talla": "M", "precio": 80, "marca": "Reebok" },
  { "nombre": "Short Deportivo", "talla": "S", "precio": 25, "marca": "Under Armour" },
  { "nombre": "Zapatillas Running", "talla": "42", "precio": 100, "marca": "New Balance" },
  { "nombre": "Tenis Casual", "talla": "41", "precio": 60, "marca": "Vans" },
  { "nombre": "Camiseta Básica", "talla": "M", "precio": 15, "marca": "Converse" },
  { "nombre": "Sudadera Retro", "talla": "L", "precio": 45, "marca": "Fila" },
  { "nombre": "Jeans", "talla": "32", "precio": 55, "marca": "Levi's" }
]
```
```json
📤 Respuesta esperada
{
  "message": "Prendas creadas correctamente"
}
```
## ✏️ Actualizar prenda

-**Método:** PUT
-**Endpoint:** /api/prendas/{id}
```json
📥 Cuerpo de la solicitud
{
  "marca": "Nike",
  "nombre": "Camiseta Deportiva",
  "precio": 25,
  "talla": "M"
}
```
## 📌 Ejemplo de URL

**http://localhost:3000/api/prendas/69c6e8042bd7fb5b68f50c60**
```json
📤 Respuesta esperada
{
  "message": "Prenda actualizada correctamente"
}
```
## ❌ Eliminar prenda

-**Método:** DELETE
-**Endpoint:** /api/prendas/{id}

## 📌 Ejemplo de URL

**http://localhost:3000/api/prendas/69c6e8042bd7fb5b68f50c69**
```json
📤 Respuesta esperada
{
  "message": "Prenda eliminada correctamente"
}
```
---

## 🔗 URL Base
`http://localhost:3000/api/prendas`

---

## 📖 Consultar prendas

**Método:** `GET`  
**Endpoint:** `/api/prendas`

**Descripción:** Obtiene la lista de todas las prendas registradas en el sistema.

### 📤 Respuesta esperada
```json
[
  {
    "_id": "ID",
    "nombre": "Camiseta Deportiva",
    "talla": "M",
    "precio": 20,
    "marca": "Nike"
  }
]
```
## ➕ Registrar múltiples prendas

-**Método:** POST
-**Endpoint:** /api/prendas/multiple

Descripción: Permite registrar varias prendas en una sola solicitud (carga masiva).
```json
📥 Cuerpo de la solicitud
[
  { "nombre": "Camiseta Deportiva", "talla": "M", "precio": 20, "marca": "Nike" },
  { "nombre": "Pantalón Jogger", "talla": "L", "precio": 35, "marca": "Adidas" },
  { "nombre": "Sudadera con Capucha", "talla": "XL", "precio": 50, "marca": "Puma" },
  { "nombre": "Chaqueta Impermeable", "talla": "M", "precio": 80, "marca": "Reebok" },
  { "nombre": "Short Deportivo", "talla": "S", "precio": 25, "marca": "Under Armour" },
  { "nombre": "Zapatillas Running", "talla": "42", "precio": 100, "marca": "New Balance" },
  { "nombre": "Tenis Casual", "talla": "41", "precio": 60, "marca": "Vans" },
  { "nombre": "Camiseta Básica", "talla": "M", "precio": 15, "marca": "Converse" },
  { "nombre": "Sudadera Retro", "talla": "L", "precio": 45, "marca": "Fila" },
  { "nombre": "Jeans", "talla": "32", "precio": 55, "marca": "Levi's" }
]
```
```json
📤 Respuesta esperada
{
  "message": "Prendas registradas correctamente"
}
```
## ✏️ Actualizar prenda

-**Método:** PUT
-**Endpoint:** /api/prendas/{id}

Descripción: Actualiza la información de una prenda específica.

```json
📥 Cuerpo de la solicitud
{
  "marca": "Nike",
  "nombre": "Camiseta Deportiva",
  "precio": 25,
  "talla": "M"
}
```
## 📌 Ejemplo de URL

**http://localhost:3000/api/prendas/69c6e8042bd7fb5b68f50c60**
```json
📤 Respuesta esperada
{
  "message": "Prenda actualizada correctamente"
}
```
## ❌ Eliminar prenda

-**Método:** DELETE
-**Endpoint:** /api/prendas/{id}

**Descripción:** Elimina una prenda del sistema.

## 📌 Ejemplo de URL

**http://localhost:3000/api/prendas/69c6e8042bd7fb5b68f50c69**
```json
📤 Respuesta esperada
{
  "message": "Prenda eliminada correctamente"
}
```
