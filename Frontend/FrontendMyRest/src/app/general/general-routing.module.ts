import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MenuComponent } from './menu/menu.component';

const routes: Routes = [
  {path: '', redirectTo:'menu', pathMatch: 'full'},
  {path: 'menu', component: MenuComponent }, 
 
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class GeneralRoutingModule { }
