import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { UserRoutingModule } from './user-routing.module';
import { ReservationComponent } from './reservation/reservation.component';
import { SharedModule } from '../shared/shared.module';
import { UserMenuComponent } from './user-menu/user-menu.component';
import { EditReservationComponent } from './edit-reservation/edit-reservation.component';
import { DeleteReservationComponent } from './delete-reservation/delete-reservation.component';


@NgModule({
  declarations: [
    ReservationComponent,
    UserMenuComponent,
    EditReservationComponent,
    DeleteReservationComponent
  ],
  imports: [
    CommonModule,
    UserRoutingModule, 
    SharedModule
  ]
})
export class UserModule { }
