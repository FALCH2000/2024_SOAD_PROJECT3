import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { UserRoutingModule } from './user-routing.module';
import { ReservationComponent } from './reservation/reservation.component';
import { SharedModule } from '../shared/shared.module';


@NgModule({
  declarations: [
    ReservationComponent
  ],
  imports: [
    CommonModule,
    UserRoutingModule, 
    SharedModule
  ]
})
export class UserModule { }
