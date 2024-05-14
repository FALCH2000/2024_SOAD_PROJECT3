import { Component, Directive, Input } from '@angular/core';
import {  FormGroup, FormBuilder, Validators, AbstractControl } from '@angular/forms';
import { RegisterService } from '../services/register.service';
import { Router } from '@angular/router';
import { Observer } from 'rxjs';

const StrongPasswordRegx: RegExp = /^(?=[^A-Z]*[A-Z])(?=[^a-z]*[a-z])(?=\D*\d).{8,}$/;

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})


export class RegisterComponent {
  registerForm: FormGroup;
  show:string="";
  security_question_list = [
    "¿Cuál es el nombre de tu primer mascota?", 
    "¿Cuál es tu color favorito?", 
    "¿En qué ciudad naciste?",
    "¿Cuál es el nombre de tu mejor amigo de la infancia?",
    "¿Cuál es el nombre de tu abuelo paterno?",
    "¿Cuál es el nombre de la calle en la que viviste de niño/a?",
    "¿Cuál es el segundo nombre de tu hermano/a?"
  ];

  username:string = "";
  password:string = "";
  first_name:string = "";
  last_name1:string = "";
  last_name2:string = "";
  security_question = "";
  security_answer = "";

  constructor(private formBuilder: FormBuilder, private registerService:RegisterService, private router: Router) { 
    this.registerForm = this.formBuilder.group({
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
      const formValues = this.registerForm.value;

      this.username = formValues.username;
      this.password = formValues.password;
      this.first_name = formValues.first_name;
      this.last_name1 = formValues.last_name1;
      this.last_name2 = formValues.last_name2;
      this.security_question = formValues.security_question;
      this.security_answer = formValues.security_answer;

      const registro = {
        "data":{
          "method": "crear-usuario",
          "username": this.username,
          "password": this.password,
          "first_name": this.first_name,
          "last_name1": this.last_name1,
          "last_name2": this.last_name2,
          "security_question":this.security_question,
          "security_answer":this.security_answer
        }
      }
      console.log(registro);
      /*this.registerService.createUser(registro).subscribe((data)=>{
        console.log("-----registro--------")
        console.log(data)
        console.log("-----registro--------")
        this.clear();
      });
*/
      const observer: Observer<any> = {
        next: (data: any) => {
          if (data.status === 200) {
            // Aquí puedes realizar acciones adicionales si la solicitud es exitosa
          }
          this.router.navigate(['authentication/login']);
          console.log(data);
        },
        error: (error: any) => {
          console.error('Error occurred:', error);
          alert("Hubo un error creando el usuario. Vuelve a intentarlo")
          this.clear();
        },
        complete: function (): void {
          throw new Error('Function not implemented.');
        }
      };
  
      this.registerService.createUser(registro).subscribe(observer);

    }
  }

  clear() {
    this.registerForm.reset();
  }
}
