import { Component, ViewEncapsulation } from '@angular/core';
import { MatTabChangeEvent } from '@angular/material/tabs';
import { VerificationService } from '../services/verification.service';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-verification',
  templateUrl: './verification.component.html',
  styleUrls: ['./verification.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class VerificationComponent {

  all_reservations_flag = false;
  passed_reservation_flag = false;
  future_reservation_flag = false;

  all_reservations:any = new Array<any>();
  displayedColumns: string[] = ['Reservation_ID', 'User_ID', 'Number_Of_People', 'Date_Reserved', 'Start_Time','End_Time'];

  clientId = "";

  constructor(private verificationService:VerificationService, private http: HttpClient,) { }

  onTabChange(event: MatTabChangeEvent) {
    console.log('Tab activo:', event.index);
    this.clientId = "";
    if(event.index === 2){
      this.verificationService.getReservaciones().subscribe((data)=>{
          console.log(data)
          this.all_reservations = data.data;
          this.all_reservations_flag = true;
      })
    }
  }

  cargarReservaciones(){

  }
}
