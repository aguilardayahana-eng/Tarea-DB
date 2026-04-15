import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { NavbarComponent } from '../../layout/navbar/navbar.component';
import { ApiService } from '../../services/api.service';

interface Usuario {
  _id: string;  // Obligatorio
  nombre: string;
  email: string;
  edad: number;
  rol: string;
}

@Component({
  selector: 'app-usuarios',
  standalone: true,
  imports: [CommonModule, FormsModule, NavbarComponent],
  templateUrl: './usuarios.html',
  styleUrls: ['./usuarios.component.scss']
})
export class Usuarios implements OnInit {
  
  usuarios: Usuario[] = [];
  searchTerm = '';
  loading = true;
  showModal = false;
  modalMode: 'create' | 'edit' = 'create';
  selectedUsuario: Usuario = { 
    _id: '', 
    nombre: '', 
    email: '', 
    edad: 0, 
    rol: 'cliente' 
  };

  constructor(
    private api: ApiService,
    public cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.loadUsuarios();
  }

  loadUsuarios() {
    this.loading = true;
    this.api.getUsuarios().subscribe({
      next: (data: any) => {
        this.usuarios = data.usuarios || data;
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Error cargando usuarios:', err);
        this.loading = false;
        alert('Error al cargar usuarios');
      }
    });
  }

  get usuariosFiltrados() {
    if (!this.searchTerm) return this.usuarios;
    return this.usuarios.filter(usuario =>
      usuario.nombre.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
      usuario.email.toLowerCase().includes(this.searchTerm.toLowerCase())
    );
  }

  openModal(mode: 'create' | 'edit', usuario?: Usuario) {
    this.modalMode = mode;
    if (mode === 'edit' && usuario) {
      this.selectedUsuario = { ...usuario };
    } else {
      this.selectedUsuario = { 
        _id: '', 
        nombre: '', 
        email: '', 
        edad: 0, 
        rol: 'cliente' 
      };
    }
    this.showModal = true;
  }

  closeModal() {
    this.showModal = false;
    this.selectedUsuario = { 
      _id: '', 
      nombre: '', 
      email: '', 
      edad: 0, 
      rol: 'cliente' 
    };
  }

  saveUsuario() {
    if (this.modalMode === 'create') {
      this.createUsuario();
    } else {
      this.updateUsuario();
    }
  }

  createUsuario() {
    this.api.crearUsuario(this.selectedUsuario).subscribe({
      next: (response) => {
        console.log('Usuario creado:', response);
        this.loadUsuarios();
        this.closeModal();
      },
      error: (err) => {
        console.error('Error creando:', err);
        alert('Error al crear usuario');
      }
    });
  }

  updateUsuario() {
    if (this.selectedUsuario._id) {
      this.api.actualizarUsuario(this.selectedUsuario._id, this.selectedUsuario).subscribe({
        next: (response) => {
          console.log('Usuario actualizado:', response);
          this.loadUsuarios();
          this.closeModal();
        },
        error: (err) => {
          console.error('Error actualizando:', err);
          alert('Error al actualizar usuario');
        }
      });
    }
  }

  // ✅ MÉTODO DELETE
  deleteUsuario(id: string) {
    if (confirm('¿Estás seguro de eliminar este usuario?')) {
      this.api.eliminarUsuario(id).subscribe({
        next: (response) => {
          console.log('Usuario eliminado:', response);
          this.loadUsuarios();
        },
        error: (err) => {
          console.error('Error eliminando:', err);
          alert('Error al eliminar usuario');
        }
      });
    }
  }
}