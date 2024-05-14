import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { AdminRoutingModule } from './admin-routing.module';
import { VerificationComponent } from './verification/verification.component';
import { SharedModule } from '../shared/shared.module';
import { AdminMenuComponent } from './admin-menu/admin-menu.component';
import { EditItemComponent } from './edit-item/edit-item.component';
import { ScheduleComponent } from './schedule/schedule.component';


@NgModule({
  declarations: [
    VerificationComponent,
    AdminMenuComponent,
    EditItemComponent,
    ScheduleComponent
  ],
  imports: [
    CommonModule,
    AdminRoutingModule,
    SharedModule
  ]
})
export class AdminModule { }
