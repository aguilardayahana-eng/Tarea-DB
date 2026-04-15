import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { NavbarComponent } from '../../layout/navbar/navbar.component';
import { ApiService } from '../../services/api.service';

interface Prenda {
  _id: string;
  marca: string;
  nombre: string;
  precio: number;
  talla: string;
}

@Component({
  selector: 'app-prendas',
  standalone: true,
  imports: [CommonModule, FormsModule, NavbarComponent],
  templateUrl: './prendas.html',
  styleUrls: ['./prendas.component.scss']
})
export class Prendas implements OnInit {

  prendas: Prenda[] = [];
  searchTerm = '';
  loading = true;

  showModal = false;
  modalMode: 'create' | 'edit' = 'create';

  selectedPrenda: Prenda = {
    _id: '',
    marca: '',
    nombre: '',
    precio: 0,
    talla: ''
  };

  constructor(
    private api: ApiService,
    public cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.loadPrendas();
  }

  loadPrendas() {
    this.loading = true;
    this.api.getPrendas().subscribe({
      next: (data: any) => {
        this.prendas = data.prendas || data;
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Error cargando prendas:', err);
        this.loading = false;
      }
    });
  }

  get prendasFiltradas() {
    if (!this.searchTerm) return this.prendas;

    return this.prendas.filter(p =>
      p.nombre.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
      p.marca.toLowerCase().includes(this.searchTerm.toLowerCase())
    );
  }

  openModal(mode: 'create' | 'edit', prenda?: Prenda) {
    console.log('🔥 CLICK FUNCIONA');
    this.modalMode = mode;

    if (mode === 'edit' && prenda) {
      this.selectedPrenda = { ...prenda };
    } else {
      this.selectedPrenda = {
        _id: '',
        marca: '',
        nombre: '',
        precio: 0,
        talla: ''
      };
    }

    this.showModal = true;
  }

  closeModal() {
    this.showModal = false;
  }

  savePrenda() {
    if (this.modalMode === 'create') {
      this.api.crearPrenda(this.selectedPrenda).subscribe({
        next: () => {
          this.loadPrendas();
          this.closeModal();
        },
        error: (err) => console.error(err)
      });
    } else {
      this.api.actualizarPrenda(this.selectedPrenda._id, this.selectedPrenda).subscribe({
        next: () => {
          this.loadPrendas();
          this.closeModal();
        },
        error: (err) => console.error(err)
      });
    }
  }

  deletePrenda(id: string) {
    if (confirm('¿Eliminar esta prenda?')) {
      this.api.eliminarPrenda(id).subscribe({
        next: () => this.loadPrendas(),
        error: (err) => console.error(err)
      });
    }
  }
}