import { Component } from '@angular/core';
import {  FormGroup, FormBuilder, Validators, AbstractControl } from '@angular/forms';
import { RegisterService } from '../services/register.service';

const StrongPasswordRegx: RegExp = /^(?=[^A-Z]*[A-Z])(?=[^a-z]*[a-z])(?=\D*\d).{8,}$/;

@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.scss']
})
export class ForgotPasswordComponent {
  renewPasswordForm: FormGroup;

  username:string = "";
  password:string = "";
  security_answer:string = "";

  constructor(private formBuilder: FormBuilder, private registerService:RegisterService) { 
    this.renewPasswordForm = this.formBuilder.group({
      username: ['', Validators.required],
      password: ['', [Validators.required, Validators.pattern(StrongPasswordRegx)]],
      passwordVerification: ['', Validators.required],
      first_name: ['', Validators.required],
      last_name1: ['', Validators.required],
      last_name2: ['', Validators.required],
      security_question: ['', Validators.required],
      security_answer: ['', Validators.required],
    });
  }

  submit() {
    if (this.renewPasswordForm.valid) {
      // Realizar acciones cuando el formulario es válido
      this.confirmPasswordValidator
      console.log("user name is " + this.renewPasswordForm.value.username);
      const formValues = this.renewPasswordForm.value;

      this.username = formValues.username;
      this.password = formValues.password;
      this.security_answer = formValues.security_answer;

      const change = {
        "method": "cambiar-contrasena",
        "username": this.username,
        "password": this.password,
        "security_answer":this.security_answer
      }
      console.log(change);
      this.registerService.createUser(change).subscribe((data)=>{
        console.log("-----registro--------")
        console.log(data)
        console.log("-----registro--------")
        this.clear();
      });

      
    }
  }

  confirmPasswordValidator(control: AbstractControl): { [key: string]: any } | null {
    const password = control.root.get('password');
    const confirmPassword = control.value;
    console.log("etse e")
    if (password && confirmPassword && password.value !== confirmPassword) {
      return { 'passwordMismatch': true };
    }
  
    return null;
  }

  clear() {
    this.renewPasswordForm.reset();
  }
}
