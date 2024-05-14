import { Component } from '@angular/core';
import { LoginService } from '../services/login.service';
import { HttpErrorResponse } from '@angular/common/http';
import { Observer } from 'rxjs';
import { Router } from '@angular/router';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {
  username : string ="";
  password : string ="";
  loginFailed: boolean= false;
  errorMessage:string = "";

  constructor(private login:LoginService, private router: Router){

  }

  submit(): void {
    console.log("user name is " + this.username)

    const observer: Observer<any> = {
      next: (data: any) => {
        if (data.status === 200) {
          // Aquí puedes realizar acciones adicionales si la solicitud es exitosa
        }
        localStorage.setItem('token',data.type)
        if(data.type === "admin"){
          this.router.navigate(['admin/admin-menu']);
        }else{
          this.router.navigate(['user/user-menu']);

        }
      },
      error: (error: any) => {
        console.error('Error occurred:', error);
        this.loginFailed = true; // Establece loginFailed en true en caso de error
      },
      complete: function (): void {
        throw new Error('Function not implemented.');
      }
    };

    this.login.logUser(this.username, this.password).subscribe(observer);
    this.clear();
  }

  clear(){
    this.username ="";
    this.password = "";
    
  }
}
