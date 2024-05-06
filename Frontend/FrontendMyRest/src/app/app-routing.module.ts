import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomepageComponent } from './homepage/homepage.component';

const routes: Routes = [
  {path: '', redirectTo:'/homepage', pathMatch: 'full'},
  {path: 'homepage', component: HomepageComponent },
  {path: 'auth', loadChildren: () => import('./authentication/authentication.module').then(m => m.AuthenticationModule)},
  {path: 'general', loadChildren: () => import('./general/general.module').then(m => m.GeneralModule)}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
