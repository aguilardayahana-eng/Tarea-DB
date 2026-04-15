import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { NavbarComponent } from '../../layout/navbar/navbar.component';
import { ApiService } from '../../services/api.service';

interface Venta {
  _id: string;
  cantidad: number;
  fecha: string;
  marca: string;
  precio: number;
  prenda: string;
}

@Component({
  selector: 'app-ventas',
  standalone: true,
  imports: [CommonModule, FormsModule, NavbarComponent],
  templateUrl: './ventas.html',
  styleUrls: ['./ventas.component.scss']
})
export class Ventas implements OnInit {

  ventas: Venta[] = [];
  searchTerm = '';
  loading = true;

  showModal = false;
  modalMode: 'create' | 'edit' = 'create';

  selectedVenta: Venta = {
    _id: '',
    cantidad: 0,
    fecha: '',
    marca: '',
    precio: 0,
    prenda: ''
  };

  constructor(
    private api: ApiService,
    public cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.loadVentas();
  }

  loadVentas() {
    this.loading = true;
    this.api.getVentas().subscribe({
      next: (data: any) => {
        this.ventas = data.ventas || data;
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: (err) => console.error(err)
    });
  }

  get ventasFiltradas() {
    if (!this.searchTerm) return this.ventas;

    return this.ventas.filter(v =>
      v.marca.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
      v.prenda.toLowerCase().includes(this.searchTerm.toLowerCase())
    );
  }

  openModal(mode: 'create' | 'edit', venta?: Venta) {
    this.modalMode = mode;

    if (mode === 'edit' && venta) {
      this.selectedVenta = { ...venta };
    } else {
      this.selectedVenta = {
        _id: '',
        cantidad: 0,
        fecha: '',
        marca: '',
        precio: 0,
        prenda: ''
      };
    }

    this.showModal = true;
  }

  closeModal() {
    this.showModal = false;
  }

  saveVenta() {
    if (this.modalMode === 'create') {
      this.api.crearVenta(this.selectedVenta).subscribe({
        next: () => this.loadVentas(),
        error: (err) => console.error(err)
      });
    } else {
      this.api.actualizarVenta(this.selectedVenta._id, this.selectedVenta).subscribe({
        next: () => this.loadVentas(),
        error: (err) => console.error(err)
      });
    }

    this.closeModal();
  }

  deleteVenta(id: string) {
    if (confirm('¿Eliminar esta venta?')) {
      this.api.eliminarVenta(id).subscribe({
        next: () => this.loadVentas(),
        error: (err) => console.error(err)
      });
    }
  }
}