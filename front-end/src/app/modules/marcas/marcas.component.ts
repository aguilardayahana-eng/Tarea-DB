import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { NavbarComponent } from '../../layout/navbar/navbar.component';
import { ApiService } from '../../services/api.service';

interface Marca {
  _id: string;
  nombre: string;
  pais: string;
}

@Component({
  selector: 'app-marcas',
  standalone: true,
  imports: [CommonModule, FormsModule, NavbarComponent],
  templateUrl: './marcas.html',
  styleUrls: ['./marcas.component.scss']
})
export class Marcas implements OnInit {

  marcas: Marca[] = [];
  searchTerm = '';
  loading = true;

  showModal = false;
  modalMode: 'create' | 'edit' = 'create';

  selectedMarca: Marca = {
    _id: '',
    nombre: '',
    pais: ''
  };

  constructor(
    private api: ApiService,
    public cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.loadMarcas();
  }

  loadMarcas() {
    this.loading = true;
    this.api.getMarcas().subscribe({
      next: (data: any) => {
        this.marcas = data.marcas || data;
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: (err) => console.error(err)
    });
  }

  get marcasFiltradas() {
    if (!this.searchTerm) return this.marcas;

    return this.marcas.filter(m =>
      m.nombre.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
      m.pais.toLowerCase().includes(this.searchTerm.toLowerCase())
    );
  }

  openModal(mode: 'create' | 'edit', marca?: Marca) {
    this.modalMode = mode;

    if (mode === 'edit' && marca) {
      this.selectedMarca = { ...marca };
    } else {
      this.selectedMarca = { _id: '', nombre: '', pais: '' };
    }

    this.showModal = true;
  }

  closeModal() {
    this.showModal = false;
  }

  saveMarca() {
    if (this.modalMode === 'create') {
      this.api.crearMarca(this.selectedMarca).subscribe({
        next: () => this.loadMarcas(),
        error: (err) => console.error(err)
      });
    } else {
      this.api.actualizarMarca(this.selectedMarca._id, this.selectedMarca).subscribe({
        next: () => this.loadMarcas(),
        error: (err) => console.error(err)
      });
    }

    this.closeModal();
  }

  deleteMarca(id: string) {
    if (confirm('¿Eliminar esta marca?')) {
      this.api.eliminarMarca(id).subscribe({
        next: () => this.loadMarcas(),
        error: (err) => console.error(err)
      });
    }
  }
}