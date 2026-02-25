// ======================================================
// CREAR BASE DE DATOS
// ======================================================
tiendaRopaDB


// ======================================================
// COLECCIÓN: USUARIOS
// ======================================================

// Insertar un usuario
db.usuarios.insertOne({
  nombre: "Ana Pérez",
  correo: "ana@email.com",
  telefono: "8888-9999",
  direccion: "Cartago"
})

// Insertar varios usuarios
db.usuarios.insertMany([
  { nombre: "Laura Sánchez", correo: "laura@email.com", telefono: "8555-1122", direccion: "San José" },
  { nombre: "Carlos Ramírez", correo: "carlos@email.com", telefono: "8444-3344", direccion: "Heredia" }
])

// Actualizar un usuario
db.usuarios.updateOne(
  { nombre: "Ana Pérez" },
  { $set: { telefono: "8999-0000" } }
)

// Eliminar un usuario
db.usuarios.deleteOne({ nombre: "Carlos Ramírez" })


// ======================================================
// COLECCIÓN: MARCAS
// ======================================================

// Insertar una marca
db.marcas.insertOne({
  nombre: "Zara",
  pais: "España",
  categoria: "Moda casual"
})

// Insertar varias marcas
db.marcas.insertMany([
  { nombre: "Nike", pais: "Estados Unidos", categoria: "Deportiva" },
  { nombre: "Adidas", pais: "Alemania", categoria: "Deportiva" },
  { nombre: "Pull&Bear", pais: "España", categoria: "Juvenil" },
  { nombre: "Forever 21", pais: "Estados Unidos", categoria: "Moda femenina" }
])

// Actualizar una marca
db.marcas.updateOne(
  { nombre: "Zara" },
  { $set: { categoria: "Moda elegante" } }
)

// Eliminar una marca
db.marcas.deleteOne({ nombre: "Forever 21" })


// ======================================================
// COLECCIÓN: PRENDAS
// ======================================================

// Insertar una prenda
db.prendas.insertOne({
  nombre: "Blusa Casual",
  marca: "Zara",
  precio: 15000,
  stock: 20,
  talla: "M"
})

// Insertar varias prendas
db.prendas.insertMany([
  { nombre: "Camiseta Deportiva", marca: "Nike", precio: 18000, stock: 15, talla: "L" },
  { nombre: "Pantalón Deportivo", marca: "Adidas", precio: 25000, stock: 10, talla: "M" },
  { nombre: "Chaqueta Juvenil", marca: "Pull&Bear", precio: 30000, stock: 8, talla: "S" },
  { nombre: "Vestido Floral", marca: "Forever 21", precio: 22000, stock: 12, talla: "M" }
])

// Actualizar el stock de una prenda
db.prendas.updateOne(
  { nombre: "Blusa Casual" },
  { $set: { stock: 18 } }
)

// Eliminar una prenda
db.prendas.deleteOne({ nombre: "Vestido Floral" })


// ======================================================
// COLECCIÓN: VENTAS
// ======================================================

// Insertar una venta
db.ventas.insertOne({
  usuario: { nombre: "Ana Pérez", correo: "ana@email.com" },
  prendas: [
    { nombre: "Blusa Casual", marca: "Zara", cantidad: 2, precio_unitario: 15000 }
  ],
  total: 30000,
  fecha: ISODate("2025-07-01")
})

// Insertar varias ventas
db.ventas.insertMany([
  {
    usuario: { nombre: "Laura Sánchez", correo: "laura@email.com" },
    prendas: [
      { nombre: "Camiseta Deportiva", marca: "Nike", cantidad: 1, precio_unitario: 18000 }
    ],
    total: 18000,
    fecha: ISODate("2025-07-02")
  },
  {
    usuario: { nombre: "Carlos Ramírez", correo: "carlos@email.com" },
    prendas: [
      { nombre: "Pantalón Deportivo", marca: "Adidas", cantidad: 1, precio_unitario: 25000 }
    ],
    total: 25000,
    fecha: ISODate("2025-07-02")
  },
  {
    usuario: { nombre: "Sofía Herrera", correo: "sofia@email.com" },
    prendas: [
      { nombre: "Chaqueta Juvenil", marca: "Pull&Bear", cantidad: 1, precio_unitario: 30000 }
    ],
    total: 30000,
    fecha: ISODate("2025-07-03")
  }
])

// Actualizar una venta
db.ventas.updateOne(
  { "usuario.nombre": "Ana Pérez" },
  { $set: { total: 32000 } }
)

// Eliminar una venta
db.ventas.deleteOne({ "usuario.nombre": "Sofía Herrera" })


// ======================================================
// CONSULTA 1
// Obtiene la cantidad total de prendas vendidas
// en una fecha específica (2025-07-02)
// ======================================================
db.ventas.aggregate([
  { $match: { fecha: ISODate("2025-07-02") } },
  { $unwind: "$prendas" },
  {
    $group: {
      _id: "$fecha",
      totalVendidas: { $sum: "$prendas.cantidad" }
    }
  }
])


// ======================================================
// CONSULTA 2
// Obtiene la lista de todas las marcas que tienen
// al menos una venta registrada
// ======================================================
db.ventas.aggregate([
  { $unwind: "$prendas" },
  {
    $group: { _id: "$prendas.marca" }
  }
])


// ======================================================
// CONSULTA 3
// Obtiene las prendas vendidas y calcula
// la cantidad restante en stock
// ======================================================
db.ventas.aggregate([
  { $unwind: "$prendas" },
  {
    $group: {
      _id: "$prendas.nombre",
      cantidadVendida: { $sum: "$prendas.cantidad" }
    }
  },
  {
    $lookup: {
      from: "prendas",
      localField: "_id",
      foreignField: "nombre",
      as: "infoPrenda"
    }
  },
  { $unwind: "$infoPrenda" },
  {
    $project: {
      prenda: "$_id",
      cantidadVendida: 1,
      stockRestante: {
        $subtract: ["$infoPrenda.stock", "$cantidadVendida"]
      }
    }
  }
])


// ======================================================
// CONSULTA 4
// Obtiene el listado de las 5 marcas más vendidas
// junto con la cantidad total de ventas
// ======================================================
db.ventas.aggregate([
  { $unwind: "$prendas" },
  {
    $group: {
      _id: "$prendas.marca",
      totalVentas: { $sum: "$prendas.cantidad" }
    }
  },
  { $sort: { totalVentas: -1 } },
  { $limit: 5 }
])