from io import BytesIO

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile
from aiogram.filters import Command
from xhtml2pdf import pisa


from app.storage import Patient, Report


router = Router()


@router.message(Command('doctor_reports'))
async def on_start(msg: Message, patient: Patient):
    reports = await Report.filter(patient=patient)

    if not reports:
        return await msg.answer('Доктора еще ничего не заключили...')

    for r in reports:
        await msg.answer(
            text=str(r),
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Получить PDF', callback_data=f'getpdf:{r.id}')],
            ]),
        )


@router.callback_query(F.data.startswith('getpdf:'))
async def on_start(callback: CallbackQuery):

    report_id = int(callback.data.split(':')[-1])

    report = await Report.get_by_id(report_id)

    data = make_pdf(report)

    await callback.message.answer_document(BufferedInputFile(data, f'Заключение {report.timestamp}.pdf'))


def make_pdf(report: Report):
    html = f'''
    <hr />
    <p style="text-align: center;"><string>Medical Report</string></p>
    <hr />
    <p style="text-align: left;">Patient</p>
    <p style="text-align: left;">Name: {report.patient.name}</p>
    <p style="text-align: left;">OMS: {report.patient.polis}</p>
    <p style="text-align: left;">Age: {report.patient.age}</p>
    <p style="text-align: left;">Sex: {report.patient.binary_sex_string}</p>
    <hr />
    <p style="text-align: left;">Doctor</p>
    <p style="text-align: left;">Name: {report.doctor.name}</p>
    <p style="text-align: left;">Speciality: {report.doctor.speciality.name}</p>
    <hr />
    <p style="text-align: left;">Report</p>
    <p style="text-align: left;">Text: {report.text}</p>
    <p style="text-align: left;">Data and time: {report.timestamp}</p>
    '''

    file = BytesIO()
    with file:
        pisa.CreatePDF(html.encode('UTF-8'), dest=file, encoding='UTF-8')
        data = file.getvalue()
    return data
