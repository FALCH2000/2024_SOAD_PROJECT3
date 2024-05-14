import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class ChatbotService {

  constructor(private http:HttpClient) {
  }

  chatMessage(message: string) {
    return this.http.get<any>(`https://us-central1-soa-project3.cloudfunctions.net/feedback-chatbot/?texto=${message}`);
  }
}
