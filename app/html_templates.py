def generate_receipt_html(transaction, company, customer=None) -> str:
    # Enhanced HTML receipt with conditional field display
    items_html = ""
    for item in transaction.items:
        qty = item.get("quantity", 1)
        price = item.get("unitPrice", item.get("price", item.get("selling_price", 0)))
        total = qty * price
        items_html += f"""
        <div class="item-row">
            <div class="item-name">{item.get('name', item.get('productName', 'Item'))}</div>
            <div class="item-details">{qty} x {price:,.2f}</div>
            <div class="item-total">{total:,.2f}</div>
        </div>
        """

    company_name = company.name if company else "Duka Lako"
    
    # Build company details section with conditional display
    company_details = []
    if company:
        if company.physical_address or company.address:
            company_details.append(company.physical_address or company.address)
        if company.phone:
            company_details.append(f"Tel: {company.phone}")
        if company.email:
            company_details.append(f"Email: {company.email}")
        if company.website:
            company_details.append(f"Website: {company.website}")
        if company.vrn_no:
            company_details.append(f"VRN No: {company.vrn_no}")
        if company.tin_no:
            company_details.append(f"TIN No: {company.tin_no}")
    
    # Add bank info to company details for receipts
    if company and company.bank_details:
        for bank in company.bank_details:
            if bank.is_active and bank.is_primary:
                company_details.append(f"Bank: {bank.bank_name} - {bank.account_number}")

    company_details_html = ""
    for detail in company_details:
        company_details_html += f"<p>{detail}</p>"

    # Build customer details section with conditional display
    customer_details = []
    if customer:
        if customer.business_name and customer.business_name != customer.name:
            customer_details.append(f"<strong>Customer:</strong> {customer.business_name}")
            if customer.contact_person:
                customer_details.append(f"Attn: {customer.contact_person}")
        else:
            customer_details.append(f"<strong>Customer:</strong> {customer.name}")
        
        if customer.customer_number:
            customer_details.append(f"Customer No: {customer.customer_number}")
        if customer.phone:
            customer_details.append(f"Tel: {customer.phone}")
        if customer.email:
            customer_details.append(f"Email: {customer.email}")
        if customer.vrn_no:
            customer_details.append(f"VRN No: {customer.vrn_no}")
        if customer.tin_no:
            customer_details.append(f"TIN No: {customer.tin_no}")
        if customer.physical_address or customer.address:
            customer_details.append(f"Address: {customer.physical_address or customer.address}")
    elif transaction.customer_name:
        customer_details.append(f"<strong>Customer:</strong> {transaction.customer_name}")

    customer_details_html = ""
    for detail in customer_details:
        customer_details_html += f"<p>{detail}</p>"

    html = f"""
    <!DOCTYPE html>
    <html lang="sw">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Receipt - {transaction.transaction_number}</title>
        <style>
            body {{
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f1f5f9;
                color: #333;
            }}
            .receipt-container {{
                max-width: 500px;
                margin: 0 auto;
                background: #fff;
                padding: 30px 20px;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            }}
            .header {{
                text-align: center;
                margin-bottom: 20px;
                border-bottom: 2px solid #25A18E;
                padding-bottom: 20px;
            }}
            .header h1 {{
                margin: 0 0 10px 0;
                color: #25A18E;
                font-size: 24px;
                font-weight: bold;
            }}
            .header p {{
                margin: 2px 0;
                font-size: 12px;
                color: #666;
            }}
            .company-details, .customer-details {{
                margin-bottom: 20px;
                font-size: 12px;
                color: #555;
                background: #f8fafc;
                padding: 15px;
                border-radius: 6px;
            }}
            .transaction-details {{
                margin-bottom: 20px;
                font-size: 12px;
                color: #555;
            }}
            .items-table {{
                width: 100%;
                border-bottom: 2px solid #eee;
                margin-bottom: 20px;
                padding-bottom: 10px;
            }}
            .item-row {{
                display: flex;
                flex-wrap: wrap;
                margin-bottom: 10px;
            }}
            .item-name {{
                flex: 1 1 100%;
                font-weight: bold;
                margin-bottom: 4px;
            }}
            .item-details {{
                flex: 1;
                color: #666;
                font-size: 12px;
            }}
            .item-total {{
                flex: 0 0 100px;
                text-align: right;
                font-weight: bold;
            }}
            .totals-row {{
                display: flex;
                justify-content: space-between;
                margin-bottom: 8px;
                font-size: 14px;
            }}
            .grand-total {{
                font-size: 18px;
                font-weight: bold;
                color: #FF6B2C;
                border-top: 2px solid #eee;
                padding-top: 10px;
                margin-top: 5px;
            }}
            .footer {{
                text-align: center;
                margin-top: 30px;
                font-size: 12px;
                color: #888;
                border-top: 1px solid #eee;
                padding-top: 20px;
            }}
            .company-logo {{
                max-width: 100px;
                max-height: 60px;
                margin-bottom: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="receipt-container">
            <div class="header">
                {f'<img src="{company.logo}" alt="Logo" class="company-logo">' if company and company.logo else ''}
                <h1>{company_name}</h1>
                {company_details_html}
            </div>
            
            {f'<div class="customer-details">{customer_details_html}</div>' if customer_details_html else ''}
            
            <div class="transaction-details">
                <p><strong>Receipt Number:</strong> {transaction.transaction_number}</p>
                <p><strong>Date:</strong> {transaction.created_at.strftime('%d-%m-%Y %H:%M')}</p>
                <p><strong>Sales Person:</strong> {transaction.cashier_name or 'Cashier'}</p>
                <p><strong>Payment Method:</strong> {transaction.payment_method.title()}</p>
            </div>
            
            <div class="items-table">
                <h3 style="margin-bottom: 15px; color: #25A18E;">Items</h3>
                {items_html}
            </div>
            
            <div class="totals-section">
                {(transaction.discount_amount or 0) > 0 and f'''
                <div class="totals-row">
                    <span>Subtotal</span>
                    <span>{company.currency_symbol if company else 'TSh'}{transaction.subtotal:,.2f}</span>
                </div>
                <div class="totals-row">
                    <span>Discount</span>
                    <span style="color: #dc2626;">-{company.currency_symbol if company else 'TSh'}{transaction.discount_amount:,.2f}</span>
                </div>
                ''' or ''}
                {(transaction.tax_amount or 0) > 0 and f'''
                <div class="totals-row">
                    <span>Tax</span>
                    <span>{company.currency_symbol if company else 'TSh'}{transaction.tax_amount:,.2f}</span>
                </div>
                ''' or ''}
                <div class="totals-row grand-total">
                    <span>Total</span>
                    <span>{company.currency_symbol if company else 'TSh'}{transaction.total:,.2f}</span>
                </div>
                <div class="totals-row">
                    <span>Amount Paid</span>
                    <span>{company.currency_symbol if company else 'TSh'}{transaction.amount_paid:,.2f}</span>
                </div>
                {transaction.amount_due > 0 and f'''
                <div class="totals-row" style="color: #d32f2f;">
                    <span>Amount Due</span>
                    <span>{company.currency_symbol if company else 'TSh'}{transaction.amount_due:,.2f}</span>
                </div>
                ''' or ''}
                {transaction.change and transaction.change > 0 and f'''
                <div class="totals-row" style="color: #16a34a;">
                    <span>Change</span>
                    <span>{company.currency_symbol if company else 'TSh'}{transaction.change:,.2f}</span>
                </div>
                ''' or ''}
            </div>
            
            {company.document_footer and f'<div style="margin-top: 20px; padding: 15px; background: #f1f5f9; border-radius: 6px; font-size: 11px; color: #666; text-align: center;">{company.document_footer}</div>' or ''}
            
            <div class="footer">
                <p>Thank you for your business!</p>
                <p style="font-size: 10px; margin-top: 10px; color: #aaa;">Powered by DUKA-SALES</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html


def generate_invoice_html(transaction, company, customer=None, terms_conditions=None) -> str:
    # Professional invoice template with conditional fields
    items_html = ""
    for item in transaction.items:
        qty = item.get("quantity", 1)
        price = item.get("unitPrice", item.get("price", 0))
        total = qty * price
        items_html += f"""
        <tr>
            <td>{item.get('name', 'Item')}</td>
            <td>{qty}</td>
            <td>{company.currency_symbol if company else 'TSh'}{price:,.2f}</td>
            <td>{company.currency_symbol if company else 'TSh'}{total:,.2f}</td>
        </tr>
        """

    # Build company details
    company_details = []
    if company:
        if company.physical_address or company.address:
            company_details.append(company.physical_address or company.address)
        if company.phone:
            company_details.append(f"Tel: {company.phone}")
        if company.email:
            company_details.append(f"Email: {company.email}")
        if company.website:
            company_details.append(f"Website: {company.website}")
        if company.vrn_no:
            company_details.append(f"VRN No: {company.vrn_no}")
        if company.tin_no:
            company_details.append(f"TIN No: {company.tin_no}")

    # Build customer and shipping details
    customer_details = []
    shipping_details = []
    
    if customer:
        if customer.business_name and customer.business_name != customer.name:
            customer_details.append(f"<strong>Customer:</strong> {customer.business_name}")
            if customer.contact_person:
                customer_details.append(f"Attn: {customer.contact_person}")
        else:
            customer_details.append(f"<strong>Customer:</strong> {customer.name}")
        
        if customer.customer_number:
            customer_details.append(f"Customer No: {customer.customer_number}")
        if customer.phone:
            customer_details.append(f"Tel: {customer.phone}")
        if customer.email:
            customer_details.append(f"Email: {customer.email}")
        if customer.vrn_no:
            customer_details.append(f"VRN No: {customer.vrn_no}")
        if customer.tin_no:
            customer_details.append(f"TIN No: {customer.tin_no}")
        if customer.physical_address or customer.address:
            customer_details.append(f"Address: {customer.physical_address or customer.address}")
        
        # Shipping details
        if customer.shipping_address or (customer.physical_address or customer.address):
            shipping_details.append(f"<strong>Ship To:</strong>")
            shipping_details.append(customer.shipping_address or customer.physical_address or customer.address)
            if customer.shipping_city or customer.city:
                shipping_details.append(f"{customer.shipping_city or customer.city}, {customer.shipping_region or customer.region}")
            if customer.shipping_country or customer.country:
                shipping_details.append(customer.shipping_country or customer.country)

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Invoice - {transaction.transaction_number}</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
            
            body {{ 
                font-family: 'Inter', sans-serif; 
                margin: 0; 
                padding: 40px 20px; 
                background: #f8fafc; 
                color: #1e293b;
                line-height: 1.5;
            }}
            .invoice-container {{ 
                max-width: 850px; 
                margin: 0 auto; 
                background: white; 
                padding: 50px; 
                border-radius: 12px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.05);
                position: relative;
                overflow: hidden;
            }}
            .invoice-container::before {{
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 8px;
                background: linear-gradient(90deg, #2563eb, #3b82f6);
            }}
            .header {{ 
                display: flex; 
                justify-content: space-between; 
                align-items: flex-start;
                margin-bottom: 40px; 
            }}
            .company-brand {{ flex: 1; }}
            .company-logo {{ 
                max-width: 180px; 
                max-height: 100px; 
                object-fit: contain;
                margin-bottom: 15px; 
            }}
            .company-name {{
                font-size: 24px;
                font-weight: 700;
                margin: 0 0 8px 0;
                color: #0f172a;
                text-transform: uppercase;
                letter-spacing: -0.02em;
            }}
            .company-info-text {{
                font-size: 13px;
                color: #64748b;
                margin: 2px 0;
            }}
            .invoice-meta {{ 
                text-align: right; 
                min-width: 220px;
            }}
            .invoice-title {{ 
                font-size: 42px; 
                font-weight: 800;
                color: #2563eb; 
                margin: 0 0 15px 0;
                letter-spacing: -0.04em;
            }}
            .meta-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 8px;
                font-size: 13px;
            }}
            .meta-label {{ font-weight: 600; color: #64748b; text-align: left; }}
            .meta-value {{ font-weight: 500; color: #1e293b; text-align: right; }}

            .address-section {{ 
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 40px;
                margin-bottom: 40px; 
                padding: 25px;
                background: #f8fafc;
                border-radius: 8px;
            }}
            .address-box h3 {{
                font-size: 11px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.1em;
                color: #64748b;
                margin: 0 0 12px 0;
            }}
            .address-name {{
                font-size: 16px;
                font-weight: 700;
                color: #0f172a;
                margin-bottom: 5px;
            }}
            .address-detail {{
                font-size: 13px;
                color: #475569;
                margin: 3px 0;
            }}

            table {{ 
                width: 100%; 
                border-collapse: separate; 
                border-spacing: 0;
                margin-bottom: 30px; 
            }}
            th {{ 
                background: #f1f5f9; 
                color: #475569;
                font-weight: 600;
                font-size: 12px;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                padding: 15px;
                text-align: left;
                border-bottom: 2px solid #e2e8f0;
            }}
            td {{ 
                padding: 15px; 
                font-size: 14px;
                border-bottom: 1px solid #f1f5f9; 
            }}
            .item-sku {{ font-size: 11px; color: #94a3b8; font-family: monospace; display: block; margin-top: 4px; }}
            
            .invoice-footer {{
                display: grid;
                grid-template-columns: 1.5fr 1fr;
                gap: 40px;
                margin-top: 20px;
            }}
            
            .payment-info h3 {{
                font-size: 14px;
                font-weight: 700;
                margin-bottom: 15px;
                color: #0f172a;
                border-bottom: 1px solid #e2e8f0;
                padding-bottom: 8px;
            }}
            .bank-card {{
                margin-bottom: 15px;
                padding: 12px;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                font-size: 12px;
            }}
            .bank-name {{ font-weight: 700; color: #2563eb; font-size: 13px; margin-bottom: 5px; }}
            .bank-detail {{ margin: 3px 0; color: #475569; }}
            .bank-detail span {{ font-weight: 600; color: #1e293b; }}

            .summary-table {{ width: 100%; }}
            .summary-row {{ display: flex; justify-content: space-between; padding: 8px 0; font-size: 14px; }}
            .summary-label {{ color: #64748b; font-weight: 500; }}
            .summary-value {{ color: #1e293b; font-weight: 600; }}
            .grand-total-row {{ 
                margin-top: 10px;
                padding-top: 15px;
                border-top: 2px solid #e2e8f0;
                font-size: 20px;
            }}
            .grand-total-label {{ color: #0f172a; font-weight: 800; }}
            .grand-total-value {{ color: #2563eb; font-weight: 800; }}

            .signature-section {{
                margin-top: 60px;
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 60px;
            }}
            .signature-box {{
                text-align: center;
            }}
            .signature-line {{
                border-top: 1px solid #cbd5e1;
                margin-bottom: 10px;
            }}
            .signature-label {{ font-size: 12px; font-weight: 600; color: #64748b; }}
            .authorized-name {{ font-size: 13px; font-weight: 700; color: #1e293b; margin-top: 5px; }}

            .terms-footer {{
                margin-top: 50px;
                padding-top: 20px;
                border-top: 1px solid #e2e8f0;
                font-size: 11px;
                color: #94a3b8;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="invoice-container">
            <div class="header">
                <div class="company-brand">
                    {f'<img src="{company.logo}" alt="Logo" class="company-logo">' if company and company.logo else ''}
                    <h2 class="company-name">{company.name if company else 'Company Name'}</h2>
                    {chr(10).join([f'<p class="company-info-text">{detail}</p>' for detail in company_details])}
                </div>
                <div class="invoice-meta">
                    <h1 class="invoice-title">INVOICE</h1>
                    <div class="meta-grid">
                        <div class="meta-label">Invoice No:</div>
                        <div class="meta-value">{transaction.transaction_number}</div>
                        <div class="meta-label">Date:</div>
                        <div class="meta-value">{transaction.created_at.strftime('%b %d, %Y')}</div>
                        <div class="meta-label">Currency:</div>
                        <div class="meta-value">{company.currency if company else 'TSH'}</div>
                    </div>
                </div>
            </div>
            
            <div class="address-section">
                <div class="address-box">
                    <h3>Invoice To</h3>
                    <div class="address-name">{customer.business_name if customer and customer.business_name else (customer.name if customer else transaction.customer_name or 'Walk-in Customer')}</div>
                    {f'<div class="address-detail">Ph: {customer.phone}</div>' if customer and customer.phone else ''}
                    {f'<div class="address-detail">Em: {customer.email}</div>' if customer and customer.email else ''}
                    {f'<div class="address-detail">{customer.physical_address or customer.address}</div>' if customer and (customer.physical_address or customer.address) else ''}
                    {f'<div class="address-detail">TIN: {customer.tin_no}</div>' if customer and customer.tin_no else ''}
                </div>
                <div class="address-box">
                    <h3>Ship To</h3>
                    {shipping_details and chr(10).join([f'<div class="address-detail">{detail}</div>' for detail in shipping_details]) or '<div class="address-detail">Same as Billing</div>'}
                </div>
            </div>
            
            <table>
                <thead>
                    <tr>
                        <th>Item Description</th>
                        <th style="text-align: center;">Qty</th>
                        <th style="text-align: right;">Unit Price</th>
                        <th style="text-align: right;">Amount</th>
                    </tr>
                </thead>
                <tbody>
                    {items_html}
                </tbody>
            </table>
            
            <div class="invoice-footer">
                <div class="payment-info">
                    {f'''
                    <h3>Payment Information</h3>
                    {''.join([f"""
                    <div class="bank-card">
                        <div class="bank-name">{bank.bank_name}</div>
                        <div class="bank-detail">Acc Name: <span>{bank.account_name}</span></div>
                        <div class="bank-detail">Acc Number: <span>{bank.account_number}</span></div>
                        {f'<div class="bank-detail">Branch: <span>{bank.branch_name}</span></div>' if bank.branch_name else ''}
                        {f'<div class="bank-detail">Mobile Money: <span>{bank.mobile_money_number}</span></div>' if bank.mobile_money_number else ''}
                    </div>
                    """ for bank in company.bank_details if bank.is_active])}
                    ''' if any(b.is_active for b in company.bank_details) else ''}
                    
                    {terms_conditions and f'''
                    <div style="margin-top: 25px;">
                        <h3 style="font-size: 12px; margin-bottom: 10px;">Terms & Conditions</h3>
                        <p style="font-size: 11px; color: #64748b; line-height: 1.6;">{terms_conditions.terms_text or terms_conditions.payment_terms or 'Please pay within terms.'}</p>
                    </div>
                    ''' or ''}
                </div>
                
                <div class="summary-section">
                    <div class="summary-row">
                        <span class="summary-label">Sub Total</span>
                        <span class="summary-value">{company.currency_symbol if company else 'TSh'}{transaction.subtotal:,.2f}</span>
                    </div>
                    {(transaction.tax_amount or 0) > 0 and f'''
                    <div class="summary-row">
                        <span class="summary-label">Tax (VAT)</span>
                        <span class="summary-value">{company.currency_symbol if company else 'TSh'}{transaction.tax_amount:,.2f}</span>
                    </div>
                    ''' or ''}
                    {(transaction.discount_amount or 0) > 0 and f'''
                    <div class="summary-row">
                        <span class="summary-label">Discount</span>
                        <span class="summary-value" style="color: #dc2626;">-{company.currency_symbol if company else 'TSh'}{transaction.discount_amount:,.2f}</span>
                    </div>
                    ''' or ''}
                    <div class="summary-row grand-total-row">
                        <span class="grand-total-label">Grand Total</span>
                        <span class="grand-total-value">{company.currency_symbol if company else 'TSh'}{transaction.total:,.2f}</span>
                    </div>
                </div>
            </div>

            <div class="signature-section">
                <div class="signature-box">
                    <div class="signature-line"></div>
                    <div class="signature-label">Customer Signature</div>
                </div>
                <div class="signature-box">
                    <div class="signature-line"></div>
                    <div class="signature-label">Authorized Signatory</div>
                    <div class="authorized-name">{company.authorised_signatory or company.name if company else ''}</div>
                </div>
            </div>
            
            <div class="terms-footer">
                <p>Thank you for your business! This is a computer-generated document.</p>
                <p style="margin-top: 5px;">Powered by DUKA-SALES System</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html

def generate_statement_html(customer, company, debts) -> str:
    # A simple, mobile-friendly HTML statement
    debts_html = ""
    for debt in debts:
        debts_html += f"""
        <div class="debt-card">
            <div class="debt-header">
                <span class="debt-ref">{debt.reference_number}</span>
                <span class="debt-date">{debt.created_at.strftime('%d-%m-%Y')}</span>
            </div>
            <div class="debt-amounts">
                <span>Deni Asili: Tsh {debt.original_amount:,.0f}</span>
                <span class="debt-remaining">Bado: Tsh {debt.remaining_amount:,.0f}</span>
            </div>
        </div>
        """

    company_name = company.name if company else "Duka Lako"
    company_phone = company.phone if company else ""

    html = f"""
    <!DOCTYPE html>
    <html lang="sw">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Mchanganuo wa Deni - {customer.name}</title>
        <style>
            body {{
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f1f5f9;
                color: #333;
            }}
            .statement-container {{
                max-width: 500px;
                margin: 0 auto;
                background: #fff;
                padding: 30px 20px;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            }}
            .header {{
                text-align: center;
                margin-bottom: 20px;
                padding-bottom: 20px;
                border-bottom: 2px solid #25A18E;
            }}
            .header h1 {{
                margin: 0 0 10px 0;
                color: #25A18E;
                font-size: 24px;
            }}
            .customer-info {{
                background: #f8fafc;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 20px;
            }}
            .customer-info h2 {{
                margin: 0 0 5px 0;
                font-size: 18px;
                color: #333;
            }}
            .summary-box {{
                background: #FF6B2C;
                color: #fff;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
                margin-bottom: 25px;
            }}
            .summary-box p {{
                margin: 0;
                font-size: 14px;
                opacity: 0.9;
            }}
            .summary-box h3 {{
                margin: 10px 0 0 0;
                font-size: 32px;
            }}
            .debt-card {{
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 15px;
            }}
            .debt-header {{
                display: flex;
                justify-content: space-between;
                margin-bottom: 10px;
                font-weight: bold;
                color: #475569;
            }}
            .debt-date {{
                color: #94a3b8;
                font-weight: normal;
                font-size: 14px;
            }}
            .debt-amounts {{
                display: flex;
                justify-content: space-between;
                font-size: 15px;
            }}
            .debt-remaining {{
                font-weight: bold;
                color: #e11d48;
            }}
            .footer {{
                text-align: center;
                margin-top: 30px;
                font-size: 14px;
                color: #888;
            }}
            .pay-btn {{
                display: block;
                width: 100%;
                padding: 15px;
                background-color: #25A18E;
                color: #fff;
                text-align: center;
                text-decoration: none;
                border-radius: 8px;
                font-weight: bold;
                margin-top: 20px;
                box-sizing: border-box;
            }}
        </style>
    </head>
    <body>
        <div class="statement-container">
            <div class="header">
                <h1>{company_name}</h1>
                <p>Mchanganuo wa Deni</p>
            </div>
            
            <div class="customer-info">
                <h2>Mteja: {customer.name}</h2>
                {f'<p style="margin:0; color:#666;">Simu: {customer.phone}</p>' if customer.phone else ''}
            </div>
            
            <div class="summary-box">
                <p>Jumla ya Deni Unalodaiwa</p>
                <h3>Tsh {customer.current_debt:,.0f}</h3>
            </div>
            
            <h3 style="color: #475569; margin-bottom: 15px;">Mchanganuo:</h3>
            
            {debts_html if debts_html else '<p style="text-align:center; color:#94a3b8;">Hakuna madeni yaliyosalia.</p>'}
            
            {f'<a href="https://wa.me/{company_phone.replace("+", "")}" class="pay-btn">Wasiliana Nasi Kulipa</a>' if company_phone else ''}
            
            <div class="footer">
                <p style="font-size: 11px; margin-top: 15px; color: #aaa;">Powered by DUKA-SALES</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html
