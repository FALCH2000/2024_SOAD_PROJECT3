import { Component } from '@angular/core';
import { ReservationService } from '../services/reservation.service';
import { HttpClient } from '@angular/common/http';

import {FormBuilder} from '@angular/forms';
import { Router } from '@angular/router';
import { Observer } from 'rxjs';

@Component({
  selector: 'app-reservation',
  templateUrl: './reservation.component.html',
  styleUrls: ['./reservation.component.scss'],
})
export class ReservationComponent {
  available_tables:any = new Array<any>();
  selected_tables:any = new Array<any>();
  selectedHour = ""
  selectedDateFormated = ""
  selectedDay = ""
  selectedTable = ""
  numberOfPeople = ""

  table_selected_list:any[] = [];

  tables_selected = this._formBuilder.group({});

  userToken:string|null;
  userVerification:boolean = false;


  constructor(private reservationService:ReservationService, private http: HttpClient,
     private _formBuilder: FormBuilder, private router: Router){
      this.userToken = localStorage.getItem('token')
     }

  ngOnInit(): void {}

  verifyUser(){
    if(this.userToken === null){
      alert("Debes loguearte nuevamente para completar la tarea")
      this.router.navigate(['homepage']);
    }else{
      this.reservationService.userIsValid(this.userToken).subscribe((data)=>{
        console.log(data)
        if(data.status === 200){
          this.userVerification = true;
          this.searchTable()
          
        }else{
          alert("Debes loguearte nuevamente para completar la tarea")
          this.router.navigate(['homepage']);
        }
        return true
      })
    }
  }

  searchTable(): void {

    const selectedDate = new Date(this.selectedDay);
    this.table_selected_list = []

    if (!isNaN(selectedDate.getTime())) {

      const year = selectedDate.getFullYear();
      const month = ('0' + (selectedDate.getMonth() + 1)).slice(-2); 
      const day = ('0' + selectedDate.getDate()).slice(-2);
      this.selectedDateFormated = `${year}-${month}-${day}`;

      this.reservationService.getCalendar(this.selectedDateFormated,this.selectedHour+":00").subscribe((data)=>{
        if(data.status === 200){
          console.log(data.data.available_tables)
          this.available_tables = data.data.available_tables;

          this.available_tables.forEach((table: { Table_ID: any; }) => {
            this.tables_selected.addControl(`table_${table.Table_ID}`, this._formBuilder.control('')); // Agrega un control al FormGroup
          });
        }
      })
    }
  }

  reserve(){
    // Obtener el valor de todas las mesas
    this.selected_tables.forEach((mesa: { Table_ID: any; Chairs: any; }) => {
      const Table_ID = mesa.Table_ID;
      const Chairs = mesa.Chairs;
      this.table_selected_list.push(mesa.Table_ID)
      console.log(`ID de la mesa: ${Table_ID}, Sillas: ${Chairs}`);
    }); 

    if(this.userToken === null){
      alert("Vuelve a loguearte para poder hacer esta petición")
    } else{
      const registro = {
        "token": this.userToken,
        "data":{
          "method": "crear-reserva",
          "number_of_people": String(this.numberOfPeople),
          "reservation_date": this.selectedDateFormated,
          "start_time": this.selectedHour,
          "selected_tables": this.table_selected_list
        }
      }
      console.log(registro);
      this.sendRequest(registro)
    }
    
  }

  sendRequest(registro:any){
    const observer: Observer<any> = {
      next: (data: any) => {
        alert(`La reserva fue creada y la respuesta del servidor fue:\n${data.response}`)
        this.clear()
        this.router.navigate(['user/reservation']);
        console.log(data);
      },
      error: (error: any) => {
        console.error('Error occurred:', error);
        alert("Hubo un error creando el usuario. Vuelve a intentarlo")
      },
      complete: function (): void {
        throw new Error('Function not implemented.');
      }
    };

    this.reservationService.createReservation(registro).subscribe(observer);

  }

  onCheckboxChange(event: any, table: any): void {
    if (event.checked) {
      console.log(`Checkbox para la mesa ${table.Table_ID} activado`);
      this.selected_tables.push(table);

    } else {
      console.log(`Checkbox para la mesa ${table.Table_ID} desactivado`);
      const index = this.selected_tables.indexOf(table); 
      if (index !== -1) {
        this.selected_tables.splice(index, 1); 
      }
    }
  }

  goBack(){
    this.selectedHour = "";
    this.selectedDay = "";
  }

  clear(){
    this.available_tables = new Array<any>();
    this.selected_tables = new Array<any>();
    this.selectedHour = ""
    this.selectedDateFormated = ""
    this.selectedDay = ""
    this.selectedTable = ""
    this.numberOfPeople = ""

    this.table_selected_list = [];

    this.tables_selected = this._formBuilder.group({});

    this.userVerification = false;
  }
}
