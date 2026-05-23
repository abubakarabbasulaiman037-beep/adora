import 'package:flutter_test/flutter_test.dart';
import 'package:adora/main.dart';

void main() {
  testWidgets('ADORA app smoke test', (WidgetTester tester) async {
    await tester.pumpWidget(const AdoraApp());
    expect(find.text('ADORA'), findsOneWidget);
  });
}
