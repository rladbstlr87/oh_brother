import React, { useState, useEffect } from 'react';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';
import axios from 'axios';
import './Calendar.css';

const Calendar = () => {
    const [events, setEvents] = useState([]);

    const fetchEvents = async (info, successCallback, failureCallback) => {
        try {
            const response = await axios.get('http://127.0.0.1:8000/api/events/', {
                params: {
                    start: info.startStr,
                    end: info.endStr,
                }
            });

            const formattedEvents = response.data.map(event => ({
                id: event.id,
                title: event.title,
                start: event.start_datetime,
                end: event.end_datetime,
                allDay: event.all_day,
                url: event.registration_url || '',
                extendedProps: {
                    location: event.location,
                    host: event.host_church_name,
                    description: event.description
                }
            }));

            successCallback(formattedEvents);
        } catch (error) {
            console.error("Error fetching events:", error);
            failureCallback(error);
        }
    };

    const handleEventClick = (info) => {
        info.jsEvent.preventDefault();
        const props = info.event.extendedProps;
        let content = `
            <h3>${info.event.title}</h3>
            <p><strong>일시:</strong> ${info.event.start?.toLocaleString()} ~ ${info.event.end?.toLocaleString() || ''}</p>
            <p><strong>장소:</strong> ${props.location}</p>
            <p><strong>주최:</strong> ${props.host}</p>
        `;

        if (props.description) {
            content += `<p class="desc">${props.description}</p>`;
        }

        if (info.event.url) {
            window.open(info.event.url, "_blank");
        } else {
            // Simple alert for now, in real app maybe a modal
            alert(`${info.event.title}\n${props.location}\n${props.host}`);
        }
    };

    return (
        <div className="calendar-container">
            <FullCalendar
                plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
                initialView="dayGridMonth"
                headerToolbar={{
                    left: 'prev,next today',
                    center: 'title',
                    right: 'dayGridMonth,timeGridWeek'
                }}
                events={fetchEvents}
                eventClick={handleEventClick}
                locale="ko"
                height="auto"
            />
        </div>
    );
};

export default Calendar;
