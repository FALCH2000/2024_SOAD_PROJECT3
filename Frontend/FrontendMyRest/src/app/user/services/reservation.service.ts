import {HttpClient, HttpHeaders} from '@angular/common/http';
import { Observable } from 'rxjs';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ReservationService {


  constructor(private http:HttpClient) { }

  getCalendar(date:string, time:string ):Observable<any>{
    var url = `https://us-central1-soa-project3.cloudfunctions.net/obtener-calendario/?date=${date}&start_time=${time}`
    return this.http.get<any>(url);
  }

  editReservation(reservation:any):Observable<any>{
    var url = 'https://us-central1-soa-project3.cloudfunctions.net/broker'
    return this.http.post<any>(url, reservation);
  }

}
