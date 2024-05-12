import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { VerificationComponent } from './verification/verification.component';

const routes: Routes = [
  {path: '', redirectTo:'verification', pathMatch: 'full'},
  {path: 'verification', component: VerificationComponent }, 
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AdminRoutingModule { }
