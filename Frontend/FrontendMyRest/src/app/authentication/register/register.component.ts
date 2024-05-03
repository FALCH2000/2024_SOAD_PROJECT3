import { Component, Directive, Input } from '@angular/core';
import {  FormGroup, FormBuilder, Validators, AbstractControl } from '@angular/forms';

const StrongPasswordRegx: RegExp = /^(?=[^A-Z]*[A-Z])(?=[^a-z]*[a-z])(?=\D*\d).{8,}$/;

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})


export class RegisterComponent {
  registerForm: FormGroup;
  show:string="";

  constructor(private formBuilder: FormBuilder) { 
    this.registerForm = this.formBuilder.group({
      username: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.pattern(StrongPasswordRegx)]],
      passwordVerification: ['', Validators.required]
    });
  }

  ngOnInit(): void {
    
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

  submit() {
    if (this.registerForm.valid) {
      // Realizar acciones cuando el formulario es válido
      this.confirmPasswordValidator
      console.log("user name is " + this.registerForm.value.username);
      this.clear();
    }
  }

  clear() {
    this.registerForm.reset();
  }
}
