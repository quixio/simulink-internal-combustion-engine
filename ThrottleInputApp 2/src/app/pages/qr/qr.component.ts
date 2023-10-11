import { Component, OnInit } from '@angular/core';

@Component({
  templateUrl: './qr.component.html',
  styleUrls: ['./qr.component.scss']
})
export class QrComponent implements OnInit {
  qrValue: string;

  constructor() { }

  ngOnInit(): void {
    const url = `${window.location.protocol}//${window.location.host}`
    this.qrValue = url;
  }

}
