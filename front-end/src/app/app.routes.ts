import { Routes } from '@angular/router';

import { DashboardComponent } from './layout/dashboard/dashboard.component';
import { Usuarios } from './modules/usuarios/usuarios.component';
import { Marcas } from './modules/marcas/marcas.component';
import { Prendas } from './modules/prendas/prendas.component';
import { Ventas } from './modules/ventas/ventas.component';
import { Reportes } from './modules/reportes/reportes.component';

export const routes: Routes = [
  { path: '', component: DashboardComponent },      
  { path: 'usuarios', component: Usuarios },        
  { path: 'marcas', component: Marcas },            
  { path: 'prendas', component: Prendas },          
  { path: 'ventas', component: Ventas },            
  { path: 'reportes', component: Reportes }         
];