from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import io

def generar_pdf_historial(historial_data, nombre_usuario):
    """
    Genera un PDF con el historial de predicciones del usuario
    
    Args:
        historial_data: Diccionario con el historial del usuario
        nombre_usuario: Nombre del usuario
    
    Returns:
        BytesIO object con el PDF generado
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a73e8'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#333333'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    normal_style = styles['Normal']
    
    # Título principal
    title = Paragraph(f"📊 Historial de Predicciones", title_style)
    elements.append(title)
    
    # Información del usuario
    user_info = Paragraph(f"<b>Usuario:</b> {nombre_usuario}<br/><b>Fecha de generación:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", normal_style)
    elements.append(user_info)
    elements.append(Spacer(1, 0.3*inch))
    
    # Resumen
    total_predicciones = len(historial_data.get('historial', []))
    summary = Paragraph(f"<b>Total de predicciones realizadas:</b> {total_predicciones}", heading_style)
    elements.append(summary)
    elements.append(Spacer(1, 0.2*inch))
    
    # Procesar cada predicción
    for idx, prediccion in enumerate(historial_data.get('historial', []), 1):
        # Encabezado de la predicción
        pred_title = Paragraph(f"<b>Predicción #{idx}</b>", heading_style)
        elements.append(pred_title)
        
        # Fecha
        fecha = prediccion.get('fecha_respuesta', 'N/A')
        fecha_text = Paragraph(f"<b>Fecha:</b> {fecha}", normal_style)
        elements.append(fecha_text)
        elements.append(Spacer(1, 0.1*inch))
        
        # Datos ingresados
        datos = prediccion.get('datos_ingresados', {})
        datos_table_data = [
            ['Parámetro', 'Respuesta del usuario'],
            ['Día de la semana', datos.get('Day_of_Week', 'N/A')],
            ['Control de cruce', datos.get('Junction_Control', 'N/A')],
            ['Detalle de cruce', datos.get('Junction_Detail', 'N/A')],
            ['Condiciones de luz', datos.get('Light_Conditions', 'N/A')],
            ['Distrito', str(datos.get('Local_Authority_District', 'N/A'))],
            ['Superficie de vía', datos.get('Road_Surface_Conditions', 'N/A')],
            ['Tipo de vía', datos.get('Road_Type', 'N/A')],
            ['Límite de velocidad', datos.get('Speed_limit', 'N/A')],
            ['Área', datos.get('Urban_or_Rural_Area', 'N/A')],
            ['Condiciones climáticas', datos.get('Weather_Conditions', 'N/A')],
            ['Tipo de vehículo', datos.get('Vehicle_Type', 'N/A')],
            ['Número de víctimas', datos.get('Number_of_Casualties', 'N/A')],
            ['Número de vehículos', datos.get('Number_of_Vehicles', 'N/A')],
        ]
        
        datos_table = Table(datos_table_data, colWidths=[3*inch, 3*inch])
        datos_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a73e8')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')])
        ]))
        
        elements.append(datos_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Resultados de predicción
        predicciones = prediccion.get('predicciones', {})
        pred_title_result = Paragraph("<b>Resultados de los Modelos:</b>", normal_style)
        elements.append(pred_title_result)
        
        pred_table_data = [
            ['Modelo', 'Predicción'],
            ['Random Forest', predicciones.get('RandomForest', 'N/A')],
            ['KNN', predicciones.get('KNN', 'N/A')],
            ['SVM', predicciones.get('SVM', 'N/A')],
        ]
        
        pred_table = Table(pred_table_data, colWidths=[2*inch, 4*inch])
        pred_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34a853')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
        ]))
        
        elements.append(pred_table)
        
        # Separador entre predicciones
        if idx < total_predicciones:
            elements.append(Spacer(1, 0.3*inch))
            elements.append(PageBreak())
    
    # Pie de página
    footer = Paragraph(
        "<i>Este documento fue generado automáticamente por el Sistema de Predicción de Severidad de Accidentes.</i>",
        ParagraphStyle('Footer', parent=normal_style, fontSize=8, textColor=colors.grey, alignment=TA_CENTER)
    )
    elements.append(Spacer(1, 0.5*inch))
    elements.append(footer)
    
    # Construir PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer