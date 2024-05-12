import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class VerificationService {

  constructor(private http:HttpClient) { }

  getReservaciones():Observable<any>{
    const url = 'https://us-central1-groovy-rope-416616.cloudfunctions.net/obtener-reservas/?time=all';
    return this.http.get<any>(url);
  }

}
