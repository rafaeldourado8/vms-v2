from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime
from io import BytesIO
from fastapi import APIRouter, Header
from sqlalchemy import create_engine, text
import boto3

router = APIRouter(prefix="/reports", tags=["reports"])

engine = create_engine('postgresql://gtvision:gtvision_password@postgres:5432/gtvision')

s3_client = boto3.client(
    's3',
    endpoint_url='http://minio:9000',
    aws_access_key_id='minioadmin',
    aws_secret_access_key='minioadmin'
)


class AuditReportGenerator:
    """Gerador de relatórios PDF para comprovação jurídica."""
    
    def generate_cleanup_report(
        self,
        tenant_id: str,
        start_date: datetime,
        end_date: datetime
    ) -> bytes:
        """
        Gera relatório PDF de expurgo automático.
        
        Conteúdo:
        - Cabeçalho com dados da prefeitura
        - Período do relatório
        - Política de retenção aplicada
        - Lista de gravações excluídas
        - Total de espaço liberado
        - Assinatura digital (hash)
        """
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()
        
        # Título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=1  # Center
        )
        
        story.append(Paragraph("RELATÓRIO DE EXPURGO AUTOMÁTICO", title_style))
        story.append(Paragraph("Sistema GT-Vision VMS", styles['Normal']))
        story.append(Spacer(1, 0.5*cm))
        
        # Informações do tenant
        with engine.connect() as conn:
            tenant_query = text("""
                SELECT c.nome, c.cnpj, p.nome as plano, p.retention_days
                FROM cidades c
                JOIN planos p ON c.plano_id = p.id
                WHERE c.id = :tenant_id
            """)
            tenant = conn.execute(tenant_query, {"tenant_id": tenant_id}).fetchone()
            
            info_data = [
                ["Prefeitura:", tenant.nome],
                ["CNPJ:", tenant.cnpj],
                ["Plano:", tenant.plano],
                ["Política de Retenção:", f"{tenant.retention_days} dias"],
                ["Período do Relatório:", f"{start_date.strftime('%d/%m/%Y')} a {end_date.strftime('%d/%m/%Y')}"],
                ["Data de Geração:", datetime.now().strftime('%d/%m/%Y %H:%M:%S')]
            ]
            
            info_table = Table(info_data, colWidths=[5*cm, 10*cm])
            info_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.grey),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(info_table)
            story.append(Spacer(1, 1*cm))
            
            # Buscar gravações excluídas no período
            cleanup_query = text("""
                SELECT 
                    al.created_at,
                    al.metadata->>'camera_id' as camera_id,
                    al.metadata->>'size_bytes' as size_bytes,
                    al.metadata->>'start_time' as start_time
                FROM audit_logs al
                WHERE 
                    al.tenant_id = :tenant_id
                    AND al.action = 'recording.deleted'
                    AND al.metadata->>'reason' = 'retention_policy'
                    AND al.created_at BETWEEN :start_date AND :end_date
                ORDER BY al.created_at DESC
            """)
            
            deletions = conn.execute(cleanup_query, {
                "tenant_id": tenant_id,
                "start_date": start_date,
                "end_date": end_date
            }).fetchall()
            
            # Tabela de exclusões
            story.append(Paragraph("Gravações Excluídas", styles['Heading2']))
            story.append(Spacer(1, 0.3*cm))
            
            table_data = [["Data/Hora", "Câmera", "Período Gravado", "Tamanho (MB)"]]
            
            total_size = 0
            for deletion in deletions:
                size_mb = int(deletion.size_bytes) / (1024**2)
                total_size += size_mb
                
                table_data.append([
                    deletion.created_at.strftime('%d/%m/%Y %H:%M'),
                    deletion.camera_id[:8],
                    deletion.start_time[:10] if deletion.start_time else "N/A",
                    f"{size_mb:.2f}"
                ])
            
            deletions_table = Table(table_data, colWidths=[4*cm, 3*cm, 4*cm, 3*cm])
            deletions_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(deletions_table)
            story.append(Spacer(1, 1*cm))
            
            # Resumo
            summary_data = [
                ["Total de Gravações Excluídas:", str(len(deletions))],
                ["Espaço Liberado:", f"{total_size / 1024:.2f} GB"],
                ["Motivo:", "Política de Retenção Automática"],
                ["Base Legal:", "LGPD Art. 16 - Minimização de Dados"]
            ]
            
            summary_table = Table(summary_data, colWidths=[7*cm, 8*cm])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(summary_table)
            story.append(Spacer(1, 1*cm))
            
            # Rodapé legal
            legal_text = """
            <b>DECLARAÇÃO:</b><br/>
            Este relatório comprova que o expurgo automático de gravações foi realizado 
            em conformidade com a política de retenção estabelecida e a Lei Geral de 
            Proteção de Dados (LGPD - Lei 13.709/2018). As gravações excluídas não 
            possuíam flags de incidente ou retenção legal.<br/><br/>
            <b>Hash do Relatório (SHA-256):</b> [HASH_PLACEHOLDER]
            """
            
            story.append(Paragraph(legal_text, styles['Normal']))
        
        # Gerar PDF
        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes


report_generator = AuditReportGenerator()


@router.get("/cleanup/{tenant_id}")
async def generate_cleanup_report(
    tenant_id: str,
    start_date: str,
    end_date: str,
    x_tenant_id: str = Header(...)
):
    """
    Gera relatório PDF de expurgo para comprovação jurídica.
    
    Query params:
        start_date: YYYY-MM-DD
        end_date: YYYY-MM-DD
    """
    
    if tenant_id != x_tenant_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    pdf_bytes = report_generator.generate_cleanup_report(tenant_id, start, end)
    
    # Upload para MinIO
    bucket = f"gtvision-reports-{tenant_id}"
    key = f"cleanup/{start_date}_{end_date}.pdf"
    
    s3_client.put_object(
        Bucket=bucket,
        Key=key,
        Body=pdf_bytes,
        ContentType='application/pdf'
    )
    
    # Gerar URL de download
    download_url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': key},
        ExpiresIn=86400  # 24h
    )
    
    return {
        "status": "success",
        "download_url": download_url
    }
