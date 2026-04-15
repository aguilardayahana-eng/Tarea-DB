import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.component.scss'],
  
})
export class DashboardComponent implements OnInit {

 usuarios: any[] = [];
  totalUsuarios = 0;
  admins = 0;
  clientes = 0;
  loading = true; 
  error = '';

  constructor(
    private api: ApiService,
    private cdr: ChangeDetectorRef  // ← OBLIGATORIO
  ) {}

  ngOnInit() {
    this.api.getUsuarios().subscribe({
      next: (data: any) => {
       this.usuarios = data.usuarios || data;
        this.totalUsuarios = this.usuarios.length;
        this.admins = this.usuarios.filter(u => u.rol === 'administrador').length;
        this.clientes = this.usuarios.length - this.admins;
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error("❌ Error:", err);
        this.error = err.message;
        this.loading = false;
        this.cdr.detectChanges();
      }
    });
  }
}