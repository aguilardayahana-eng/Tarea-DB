import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NavbarComponent } from '../../layout/navbar/navbar.component';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-reportes',
  standalone: true,
  imports: [CommonModule, NavbarComponent],
  templateUrl: './reportes.html',
  styleUrls: ['./reportes.component.scss']
})
export class Reportes implements OnInit {

  totalVentas = 0;
  totalMarcas = 0;
  totalPrendas = 0;

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.loadReportes();
  }

  loadReportes() {
    this.api.getVentas().subscribe((v: any) => {
      this.totalVentas = v.length || v.ventas?.length || 0;
    });

    this.api.getMarcas().subscribe((m: any) => {
      this.totalMarcas = m.length || m.marcas?.length || 0;
    });

    this.api.getPrendas().subscribe((p: any) => {
      this.totalPrendas = p.length || p.prendas?.length || 0;
    });
  }
}