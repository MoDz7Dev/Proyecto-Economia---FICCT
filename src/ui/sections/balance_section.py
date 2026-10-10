import flet as ft


class BalanceSection(ft.Container):
    """
    Simple balance dashboard with mock data to illustrate graphs and tables.
    """

    def __init__(
        self,
        page: ft.Page,
        bg_color: str,
        card_color: str,
        accent: str,
        accent_alt: str,
        card_accent_1: str,
        card_accent_2: str,
    ):
        super().__init__(expand=True, padding=15)

        self.page = page
        self.bg_color = bg_color
        self.card_color = card_color
        self.accent = accent
        self.accent_alt = accent_alt
        self.card_accent_1 = card_accent_1
        self.card_accent_2 = card_accent_2

        # Mock data to feed the charts and tables
        self.bank_accounts = [
            {"bank": "Banco Unión", "account": "123-456-00", "type": "Cuenta Corriente", "balance": 250_000.50},
            {"bank": "Banco Ganadero", "account": "789-321-11", "type": "Cuenta Ahorro", "balance": 180_450.30},
            {"bank": "Banco Mercantil", "account": "654-987-22", "type": "Cuenta Corriente", "balance": 95_780.10},
        ]
        self.monthly_cashflow = [
            ("Ene", 120_000, 92_000),
            ("Feb", 135_000, 101_500),
            ("Mar", 142_500, 115_000),
            ("Abr", 128_000, 97_500),
            ("May", 150_500, 120_200),
            ("Jun", 160_300, 123_800),
            ("Jul", 152_700, 118_000),
            ("Ago", 145_800, 110_900),
            ("Sep", 170_200, 130_400),
            ("Oct", 165_000, 129_500),
            ("Nov", 172_000, 135_300),
            ("Dic", 180_500, 140_000),
        ]
        self.invoices = [
            {"id": "FAC-1023", "client": "Distribuidora Andina", "amount": 18_500, "status": "Pendiente"},
            {"id": "FAC-1041", "client": "Tiendas Norte", "amount": 12_200, "status": "Pagada"},
            {"id": "FAC-1055", "client": "Hotel Sol", "amount": 9_800, "status": "Vencida"},
            {"id": "FAC-1070", "client": "Farmacias Centro", "amount": 7_600, "status": "Pendiente"},
        ]
        self.collections = [
            {"id": "COB-2001", "client": "Alimentos SRL", "amount": 6_500, "due": "15 días"},
            {"id": "COB-2004", "client": "Mercado Abasto", "amount": 4_800, "due": "30 días"},
            {"id": "COB-2010", "client": "Restaurante La Paz", "amount": 3_400, "due": "45 días"},
            {"id": "COB-2015", "client": "Minimarket Sur", "amount": 5_200, "due": "60 días"},
        ]
        self.aging_receivables = [
            ("0-30 días", 32_000),
            ("31-60 días", 18_500),
            ("61-90 días", 9_400),
            ("90+ días", 4_200),
        ]
        self.aging_payables = [
            ("0-30 días", 21_000),
            ("31-60 días", 12_800),
            ("61-90 días", 6_900),
            ("90+ días", 3_100),
        ]

        # Build UI
        self.content = ft.Column(
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Text("Balance general y flujo", size=22, weight="bold", color="white"),
                self._build_summary_cards(),
                self._build_accounts_and_cashflow(),
                self._build_invoices_and_collections(),
                self._build_aging_bars(),
            ],
        )

    # ---- Builders ----
    def _build_summary_cards(self) -> ft.Row:
        ingresos = sum(m[1] for m in self.monthly_cashflow[-3:])
        gastos = sum(m[2] for m in self.monthly_cashflow[-3:])
        utilidad = ingresos - gastos
        return ft.Row(
            spacing=10,
            run_spacing=10,
            controls=[
                self._summary_card("Ingresos 3M", ingresos, self.card_accent_1, "Entrada promedio reciente"),
                self._summary_card("Gastos 3M", gastos, self.card_accent_2, "Salidas promedio reciente"),
                self._summary_card("Utilidad 3M", utilidad, self.accent, "Ingresos - Gastos"),
            ],
        )

    def _summary_card(self, title: str, amount: float, color: str, subtitle: str) -> ft.Container:
        return ft.Container(
            expand=True,
            bgcolor=self.card_color,
            padding=15,
            border_radius=12,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK)),
            content=ft.Column(
                spacing=6,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Text(title, color="white", size=14, weight="bold"),
                    ft.Text(self._format_currency(amount), color=color, size=22, weight="bold"),
                    ft.Text(subtitle, color=ft.Colors.GREY, size=12),
                ],
            ),
        )

    def _build_accounts_and_cashflow(self) -> ft.ResponsiveRow:
        accounts_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Banco", color="white")),
                ft.DataColumn(ft.Text("Cuenta", color="white")),
                ft.DataColumn(ft.Text("Tipo", color="white")),
                ft.DataColumn(ft.Text("Saldo", color="white")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(acc["bank"], color="white")),
                        ft.DataCell(ft.Text(acc["account"], color="white")),
                        ft.DataCell(ft.Text(acc["type"], color="white")),
                        ft.DataCell(ft.Text(self._format_currency(acc["balance"]), color=self.accent)),
                    ]
                )
                for acc in self.bank_accounts
            ],
            heading_row_color=ft.Colors.with_opacity(0.1, "white"),
            data_row_color={"hovered": ft.Colors.with_opacity(0.05, "white")},
            divider_thickness=0,
        )

        cashflow_chart = self._double_bar_chart(
            title="Ingresos vs Gastos por mes",
            data=self.monthly_cashflow,
            color_a=self.accent,
            color_b=self.accent_alt,
            label_a="Ingresos",
            label_b="Gastos",
        )

        return ft.ResponsiveRow(
            columns=12,
            spacing=10,
            controls=[
                ft.Container(
                    col={"xs": 12, "md": 5},
                    bgcolor=self.card_color,
                    border_radius=12,
                    padding=12,
                    content=ft.Column(
                        spacing=8,
                        controls=[
                            ft.Text("Cuentas bancarias", color="white", weight="bold", size=16),
                            accounts_table,
                        ],
                    ),
                ),
                ft.Container(
                    col={"xs": 12, "md": 7},
                    bgcolor=self.card_color,
                    border_radius=12,
                    padding=12,
                    content=cashflow_chart,
                ),
            ],
        )

    def _build_invoices_and_collections(self) -> ft.ResponsiveRow:
        invoices_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Documento", color="white")),
                ft.DataColumn(ft.Text("Cliente", color="white")),
                ft.DataColumn(ft.Text("Monto", color="white")),
                ft.DataColumn(ft.Text("Estado", color="white")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(item["id"], color="white")),
                        ft.DataCell(ft.Text(item["client"], color="white")),
                        ft.DataCell(ft.Text(self._format_currency(item["amount"]), color="white")),
                        ft.DataCell(self._status_chip(item["status"])),
                    ]
                )
                for item in self.invoices
            ],
            heading_row_color=ft.Colors.with_opacity(0.1, "white"),
            divider_thickness=0,
        )

        collections_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Cobro", color="white")),
                ft.DataColumn(ft.Text("Cliente", color="white")),
                ft.DataColumn(ft.Text("Monto", color="white")),
                ft.DataColumn(ft.Text("Vence en", color="white")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(item["id"], color="white")),
                        ft.DataCell(ft.Text(item["client"], color="white")),
                        ft.DataCell(ft.Text(self._format_currency(item["amount"]), color="white")),
                        ft.DataCell(ft.Text(item["due"], color=self.accent_alt)),
                    ]
                )
                for item in self.collections
            ],
            heading_row_color=ft.Colors.with_opacity(0.1, "white"),
            divider_thickness=0,
        )

        return ft.ResponsiveRow(
            columns=12,
            spacing=10,
            controls=[
                ft.Container(
                    col={"xs": 12, "md": 6},
                    bgcolor=self.card_color,
                    border_radius=12,
                    padding=12,
                    content=ft.Column(
                        spacing=6,
                        controls=[
                            ft.Text("Facturas", color="white", weight="bold", size=16),
                            invoices_table,
                        ],
                    ),
                ),
                ft.Container(
                    col={"xs": 12, "md": 6},
                    bgcolor=self.card_color,
                    border_radius=12,
                    padding=12,
                    content=ft.Column(
                        spacing=6,
                        controls=[
                            ft.Text("Cobros programados", color="white", weight="bold", size=16),
                            collections_table,
                        ],
                    ),
                ),
            ],
        )

    def _build_aging_bars(self) -> ft.ResponsiveRow:
        receivables_chart = self._single_bar_chart(
            title="Antigüedad por cobrar",
            data=self.aging_receivables,
            color=self.accent,
        )
        payables_chart = self._single_bar_chart(
            title="Antigüedad por pagar",
            data=self.aging_payables,
            color=self.card_accent_2,
        )
        return ft.ResponsiveRow(
            columns=12,
            spacing=10,
            controls=[
                ft.Container(
                    col={"xs": 12, "md": 6},
                    bgcolor=self.card_color,
                    border_radius=12,
                    padding=12,
                    content=receivables_chart,
                ),
                ft.Container(
                    col={"xs": 12, "md": 6},
                    bgcolor=self.card_color,
                    border_radius=12,
                    padding=12,
                    content=payables_chart,
                ),
            ],
        )

    # ---- Helpers ----
    def _status_chip(self, status: str) -> ft.Container:
        color_map = {
            "Pendiente": self.card_accent_2,
            "Pagada": self.accent,
            "Vencida": ft.Colors.RED,
        }
        return ft.Container(
            bgcolor=ft.Colors.with_opacity(0.2, color_map.get(status, "white")),
            padding=ft.padding.symmetric(horizontal=10, vertical=4),
            border_radius=20,
            content=ft.Text(status, color=color_map.get(status, "white"), size=12, weight="bold"),
        )

    def _format_currency(self, value: float) -> str:
        return f"Bs {value:,.2f}"

    def _single_bar_chart(self, title: str, data: list[tuple[str, float]], color: str) -> ft.Column:
        max_value = max((v for _, v in data), default=1)
        bars = []
        for label, value in data:
            height = max(12, int((value / max_value) * 180))
            bars.append(
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            width=40,
                            height=height,
                            bgcolor=color,
                            border_radius=10,
                            alignment=ft.alignment.bottom_center,
                            content=ft.Text(self._format_currency(value), size=10, color="white", text_align="center"),
                        ),
                        ft.Text(label, color="white", size=12),
                    ],
                )
            )
        return ft.Column(
            spacing=8,
            controls=[
                ft.Text(title, color="white", weight="bold", size=16),
                ft.Row(controls=bars, alignment=ft.MainAxisAlignment.SPACE_AROUND, vertical_alignment=ft.CrossAxisAlignment.END),
            ],
        )

    def _double_bar_chart(
        self,
        title: str,
        data: list[tuple[str, float, float]],
        color_a: str,
        color_b: str,
        label_a: str,
        label_b: str,
    ) -> ft.Column:
        max_value = max((max(a, b) for _, a, b in data), default=1)

        def bar(value: float, color: str) -> ft.Container:
            height = max(12, int((value / max_value) * 160))
            return ft.Container(
                width=20,
                height=height,
                bgcolor=color,
                border_radius=8,
                alignment=ft.alignment.bottom_center,
                content=ft.Text(f"{value/1000:.1f}k", size=9, color="white"),
            )

        month_bars = []
        for month, inc, exp in data:
            month_bars.append(
                ft.Column(
                    spacing=4,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Row(
                            spacing=6,
                            vertical_alignment=ft.CrossAxisAlignment.END,
                            controls=[
                                bar(inc, color_a),
                                bar(exp, color_b),
                            ],
                        ),
                        ft.Text(month, color="white", size=11),
                    ],
                )
            )

        legend = ft.Row(
            spacing=12,
            controls=[
                self._legend_chip(color_a, label_a),
                self._legend_chip(color_b, label_b),
            ],
        )

        return ft.Column(
            spacing=8,
            controls=[
                ft.Text(title, color="white", weight="bold", size=16),
                legend,
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.END,
                    controls=month_bars,
                ),
            ],
        )

    def _legend_chip(self, color: str, label: str) -> ft.Row:
        return ft.Row(
            spacing=6,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(width=14, height=14, bgcolor=color, border_radius=4),
                ft.Text(label, color="white", size=12),
            ],
        )

