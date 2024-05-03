import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoginComponent } from './login/login.component';

import { AuthenticationRoutingModule } from './authentication-routing.module';
import { StrongPasswordDirective } from '../directives/strong-password.directive';


import { SharedModule } from '../shared/shared.module';
import { RegisterComponent } from './register/register.component';
import { ReactiveFormsModule } from '@angular/forms';


@NgModule({
  declarations: [
    LoginComponent,
    RegisterComponent,
    StrongPasswordDirective
  ],
  imports: [
    SharedModule,
    AuthenticationRoutingModule,
    ReactiveFormsModule
  ]
})
export class AuthenticationModule { }
