import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { VerificationComponent } from './verification/verification.component';
import { AdminMenuComponent } from './admin-menu/admin-menu.component';
import { EditItemComponent } from './edit-item/edit-item.component';
import { ScheduleComponent } from './schedule/schedule.component';

const routes: Routes = [
  {path: '', redirectTo:'admin-menu', pathMatch: 'full'},
  {path: 'verification', component: VerificationComponent }, 
  {path: 'admin-menu', component: AdminMenuComponent }, 
  {path: 'edit-item-admin', component: EditItemComponent }, 
  {path: 'new-schedule', component: ScheduleComponent }, 
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AdminRoutingModule { }
