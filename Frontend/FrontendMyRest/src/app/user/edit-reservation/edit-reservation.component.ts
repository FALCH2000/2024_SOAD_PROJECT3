import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import {EditItemService} from "../../admin/services/edit-item.service";
import {HttpClient} from "@angular/common/http";
import {Router} from "@angular/router";
import {VerificationService} from "../../admin/services/verification.service";
import {MatTabChangeEvent} from "@angular/material/tabs";

@Component({
  selector: 'app-edit-reservation',
  templateUrl: './edit-reservation.component.html',
  styleUrls: ['./edit-reservation.component.scss']
})
export class EditReservationComponent implements OnInit{
  all_reservations_flag = false;
  passed_reservation_flag = false;
  future_reservation_flag = false;

  all_reservations:any = new Array<any>();
  future_reservations:any = new Array<any>();
  displayedColumns: string[] = ['Reservation_ID', 'User_ID', 'Number_Of_People', 'Date_Reserved', 'Start_Time','End_Time'];
  username;

  constructor(private verificationService:VerificationService, private http: HttpClient,private router:Router) {
    this.username = localStorage.getItem('username');
    console.log(this.username);
  }

  ngOnInit(){
    localStorage.removeItem('reservation_id');
    if(this.username){
      this.searchPastReservations()
      this.searchFutureReservations()
    }
  }

  onTabChange(event: MatTabChangeEvent) {
    console.log('Tab activo:', event.index);
    this.clearData();
    if(event.index === 2){
      this.verificationService.getReservaciones().subscribe((data)=>{
        console.log(data)
        this.all_reservations = data.data;
        this.all_reservations_flag = true;
      })
    }
  }

  searchPastReservations(){
    if(!this.username)return;
    console.log(`Buscando reservacion pasada de cliente: ${this.username}`);
    this.clearData();
    this.verificationService.getReservaciones().subscribe((data)=>{
      console.log(data)
      this.all_reservations = data.data.filter((reservation:any)=>{
        return reservation.User_ID === this.username && this.isStartDatePast(new Date(reservation.Date_Reserved))
      });
      this.passed_reservation_flag = true;
    })
  }

  searchFutureReservations(){
    if(!this.username)return;
    console.log(`Buscando reservacion futura de cliente: ${this.username}`);
    this.clearData();
    this.verificationService.getReservaciones().subscribe((data)=>{
      console.log(data)
      this.future_reservations = data.data.filter((reservation:any)=>{
        return reservation.User_ID === this.username && !this.isStartDatePast(new Date(reservation.Date_Reserved))
      });
      this.future_reservation_flag = true;
    })
  }

  isStartDatePast(startDate: Date): boolean {
    const currentDate = new Date();
    return startDate < currentDate;
  }

  editItem(reservation_id:string){
    localStorage.setItem('reservation_id', reservation_id);
    this.router.navigate(['admin/edit-item-admin']);

  }

  clearData(){
    this.all_reservations = {};
    this.passed_reservation_flag = false;
    this.future_reservation_flag = false;
    this.all_reservations_flag = false;
  }

  protected readonly localStorage = localStorage;
}
