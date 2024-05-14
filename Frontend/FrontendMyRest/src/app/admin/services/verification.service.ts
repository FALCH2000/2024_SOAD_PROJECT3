import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class VerificationService {

  constructor(private http:HttpClient) { }

  getReservaciones():Observable<any>{
    const url = 'https://us-central1-soa-project3.cloudfunctions.net/obtener-reserva/?time=all';
    return this.http.get<any>(url);
  }

  getReservacionesPasadas(client1:string):Observable<any>{
    const url = `https://us-central1-soa-project3.cloudfunctions.net/obtener-reservas/?time=pasadas&user_id=${client1}`;
    return this.http.get<any>(url);
  }

  getReservacionesFuturas(client1:string):Observable<any>{
    const url = `https://us-central1-soa-project3.cloudfunctions.net/obtener-reservas/?time=futuras&user_id=${client1}`;
    return this.http.get<any>(url);
  }
}
