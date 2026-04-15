import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private API_URL = 'http://localhost:3000/api';

  constructor(private http: HttpClient) {}

  // =========================
  // 👥 USUARIOS
  // =========================
  getUsuarios(): Observable<any> {
    return this.http.get(`${this.API_URL}/usuarios`);
  }

  crearUsuario(data: any): Observable<any> {
    return this.http.post(`${this.API_URL}/usuarios`, data);
  }

updateUsuario(id: string, usuario: any) {
  return this.http.put(`${this.API_URL}/usuarios/${id}`, usuario, {
    headers: { 'Content-Type': 'application/json' }
  });
}

  eliminarUsuario(id: string): Observable<any> {
    return this.http.delete(`${this.API_URL}/usuarios/${id}`);
  }


  // =========================
  // 🏷️ MARCAS
  // =========================
  getMarcas(): Observable<any> {
    return this.http.get(`${this.API_URL}/marcas`);
  }

  crearMarca(data: any): Observable<any> {
    return this.http.post(`${this.API_URL}/marcas`, data);
  }

  actualizarMarca(id: string, data: any): Observable<any> {
    return this.http.put(`${this.API_URL}/marcas/${id}`, data);
  }

  eliminarMarca(id: string): Observable<any> {
    return this.http.delete(`${this.API_URL}/marcas/${id}`);
  }


  // =========================
  // 👕 PRENDAS
  // =========================
  getPrendas(): Observable<any> {
    return this.http.get(`${this.API_URL}/prendas`);
  }

  crearPrenda(data: any): Observable<any> {
    return this.http.post(`${this.API_URL}/prendas`, data);
  }

  actualizarPrenda(id: string, data: any): Observable<any> {
    return this.http.put(`${this.API_URL}/prendas/${id}`, data);
  }

  eliminarPrenda(id: string): Observable<any> {
    return this.http.delete(`${this.API_URL}/prendas/${id}`);
  }


  // =========================
  // 💰 VENTAS
  // =========================
  getVentas(): Observable<any> {
    return this.http.get(`${this.API_URL}/ventas`);
  }

  crearVenta(data: any): Observable<any> {
    return this.http.post(`${this.API_URL}/ventas`, data);
  }

  actualizarVenta(id: string, data: any): Observable<any> {
    return this.http.put(`${this.API_URL}/ventas/${id}`, data);
  }

  eliminarVenta(id: string): Observable<any> {
    return this.http.delete(`${this.API_URL}/ventas/${id}`);
  }

}