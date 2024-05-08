import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MenuComponent } from './menu/menu.component';
import { FeedbackComponent } from './feedback/feedback.component';

const routes: Routes = [
  {path: '', redirectTo:'menu', pathMatch: 'full'},
  {path: 'menu', component: MenuComponent }, 
  {path: 'feedback', component: FeedbackComponent }, 
 
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class GeneralRoutingModule { }
