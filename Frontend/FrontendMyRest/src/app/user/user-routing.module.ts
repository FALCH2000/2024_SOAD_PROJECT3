import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ReservationComponent } from './reservation/reservation.component';
import { UserMenuComponent } from './user-menu/user-menu.component';

const routes: Routes = [
  {path: '', redirectTo:'user-menu', pathMatch: 'full'},
  {path: 'reservation', component: ReservationComponent }, 
  {path: 'user-menu', component: UserMenuComponent }, 
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class UserRoutingModule { }
