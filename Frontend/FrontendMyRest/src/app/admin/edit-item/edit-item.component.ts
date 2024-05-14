import {Component, OnInit} from '@angular/core';
import { EditItemService } from '../services/edit-item.service';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-edit-item',
  templateUrl: './edit-item.component.html',
  styleUrls: ['./edit-item.component.scss']
})
export class EditItemComponent implements OnInit{
  user_reservation_id:string|null="";
  reservationForm: FormGroup;

  //Reservation data
  username:string="";
  dateReserved:string="";
  end_time:string="";
  start_time:string="";
  numberOfPeople:number=0;
  reservation_data:any = new Array<any>();


  constructor(private editItemService:EditItemService, private http: HttpClient,private router:Router, private fb: FormBuilder) {
    this.reservationForm = this.fb.group({
      username: [{ value: '', disabled: false }, Validators.required],
      dateReserved: [{ value: null, disabled: false }, Validators.required],
      startTime: [{ value: '', disabled: false }, Validators.required],
      endTime: [{ value: '', disabled: false }, Validators.required],
      numberOfPeople: [{ value: '', disabled: false }, Validators.required]
    });
    this.reservationForm.get('username')?.disable();

  }

  ngOnInit(){
    this.user_reservation_id=localStorage.getItem('reservation_id');
    this.getItem(this.user_reservation_id)
  }

  getItem(reservation_id:string|null){
    this.username = "USUARIO"
    console.log(reservation_id)
    if(reservation_id=== null){
      alert("Hubo un error obteniendo los datos de esta reserva.")
      this.router.navigate(['admin/verification']);
    }else{
      this.editItemService.getItemInfo(reservation_id).subscribe((data)=>{
        console.log(data)
        this.username = data.data.Username
        this.dateReserved = data.data.Date_Reserved
        this.end_time=data.data.End_Time
        this.start_time = data.data.Start_Time
        this.numberOfPeople = data.data.Number_Of_People
    });

    }
  }

  updateValue(){


  }
  onSubmit():void{
    const year = this.reservationForm.get('dateReserved')?.value.getFullYear();
    const month = ('0' + (this.reservationForm.get('dateReserved')?.value.getMonth() + 1)).slice(-2);
    const day = ('0' + this.reservationForm.get('dateReserved')?.value.getDate()).slice(-2);
    const selectedDateFormatted = `${year}-${month}-${day}`;
    const json = {
      "method" : "editar-reserva",
      "reservation_id":this.user_reservation_id,
      "dateReserved":selectedDateFormatted,
      "startTime":this.reservationForm.get('startTime')?.value,
      "endTime":this.reservationForm.get('endTime')?.value,
      "numberOfPeople":this.reservationForm.get('numberOfPeople')?.value,
      "selected_tables": [1,2]
    }
    this.editItemService.editReservation(json).subscribe((data)=>{
      console.log("Reservation Edited ", data)
    });

  }
}
