import { Component } from '@angular/core';
import { ChatbotService } from '../services/chatbot.service';

@Component({
  selector: 'app-feedback',
  templateUrl: './feedback.component.html',
  styleUrls: ['./feedback.component.scss']
})
export class FeedbackComponent {

  constructor(private chatbot:ChatbotService) {
    }

    allMessages: any[] = [];
    newMessage: string = '';

  sendMessage() {
      const message = this.newMessage;
      this.chatbot.chatMessage(message).subscribe((response:any) => {
          
          this.allMessages.push({message, isUser: true});
          this.allMessages.push({message: response.data, isUser: false});
          console.log(response);
      });
      this.newMessage = '';
  }
}
