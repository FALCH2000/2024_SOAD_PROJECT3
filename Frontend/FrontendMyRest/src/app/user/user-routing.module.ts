import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ReservationComponent } from './reservation/reservation.component';

const routes: Routes = [
  {path: '', redirectTo:'reservation', pathMatch: 'full'},
  {path: 'reservation', component: ReservationComponent }, 
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class UserRoutingModule { }
